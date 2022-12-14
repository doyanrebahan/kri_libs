from datetime import datetime
from urllib.parse import urljoin

from logging import Handler, LogRecord, NOTSET

import requests
from rest_framework.exceptions import APIException

from kri_lib.conf import settings
from .document import LogError
from .notification import notify_to_slack
from .utils import (
    get_request_body,
    to_preserve,
    get_traceback_info,
    get_git_branch,
    get_git_blame_email
)


class BaseKunciLogHandler(Handler):
    SAFE_KEY_HEADER = ['Authorization']
    SAFE_KEY_BODY = ['password']

    def __init__(self, level=NOTSET):
        super(BaseKunciLogHandler, self).__init__(level)

    def emit(self, record: LogRecord) -> None:
        """
        Emit a record.

        If a formatter is specified, it is used to format the record.
        The record is then written to the stream with a trailing newline.  If
        exception information is present, it is formatted using
        traceback.print_exception and appended to the stream.  If the stream
        has an 'encoding' attribute, it is used to determine how to do the
        output to the stream.
        """
        try:
            self.record_error(record)
        except RecursionError:  # See issue 36272
            raise
        except Exception:
            self.handleError(record)

    def prepare_save(self, record: LogRecord):
        request = record.request
        if request.method == 'GET':
            payload = request.GET
        else:
            body = get_request_body(request)
            payload = to_preserve(body.copy(), self.SAFE_KEY_BODY)
        stack_traces = self.format(record)
        stack_traces = stack_traces.split('\n')
        return {
            "service_name": settings.LOGGING.get('SERVICE_NAME'),
            "api_id": request.api_id,
            "url": request.get_full_path(),
            "method": request.method,
            "headers": to_preserve(
                dict(request.headers.copy()),
                self.SAFE_KEY_HEADER
            ),
            "payload": payload,
            "stack_traces": stack_traces,
            "timestamp": datetime.now()
        }

    def record_error(self, record: LogRecord):
        raise NotImplementedError("record_error() must be overriden.")


class KunciLogAPIHandler(BaseKunciLogHandler):

    def get_reports_payload(self, record: LogRecord) -> dict:
        _, exc_instance, tb = record.exc_info
        tb_info = get_traceback_info(tb)
        email = get_git_blame_email(
            file_path=tb_info.get('file'),
            line_number=tb_info.get('line_number')
        )
        return {
            'repr_exc': repr(exc_instance),
            'email': email,
            'branch': get_git_branch()
        }

    def record_error(self, record: LogRecord):
        url = urljoin(
            settings.LOGGING.get('API').get('host'),
            '/api/v1/log/log-error'
        )
        payload = self.prepare_save(record).copy()
        payload['timestamp'] = str(payload['timestamp'])
        payload['reports'] = self.get_reports_payload(record)
        response = requests.post(
            url=url,
            json=payload,
            headers={
                'Authorization': settings.LOGGING.get('API').get('Authorization')
            }
        )
        return response


class KunciDBLogHandler(BaseKunciLogHandler):

    def record_error(self, record: LogRecord):
        request = record.request
        payload = self.prepare_save(record)
        log = LogError()
        for key, value in payload.items():
            setattr(log, key, value)
        log.save()
        stack_traces = self.format(record)

        try:
            exc_class, exc_instance, tb = record.exc_info
        except TypeError:
            return log
        if not isinstance(exc_instance, APIException):
            notify_to_slack(exc_instance, tb, stack_traces, request.get_full_path())
        return log
