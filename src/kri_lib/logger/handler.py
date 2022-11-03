from logging import Handler, LogRecord, NOTSET

from rest_framework.exceptions import APIException

from kri_lib.conf import settings
from .document import LogError
from .notification import notify_to_slack
from .utils import get_request_body, to_preserve


class KunciDBLogHandler(Handler):

    SAFE_KEY_HEADER = ['Authorization']
    SAFE_KEY_BODY = ['password']

    def __init__(self, level=NOTSET):
        super(KunciDBLogHandler, self).__init__(level)

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

    def record_error(self, record: LogRecord):
        request = record.request
        log = LogError()
        log.service_name = settings.LOGGING.get('SERVICE_NAME')
        log.api_id = request.api_id
        log.url = request.get_full_path()
        log.method = request.method
        log.headers = to_preserve(
            dict(request.headers.copy()),
            self.SAFE_KEY_HEADER
        )
        if request.method == 'GET':
            log.payload = request.GET
        else:
            body = get_request_body(request)
            log.payload = to_preserve(
                body.copy(),
                self.SAFE_KEY_BODY
            )
        stack_traces = self.format(record)
        log.stack_traces = stack_traces.split('\n')
        log.save()
        try:
            exc_class, exc_instance, tb = record.exc_info
        except TypeError:
            return log
        if not isinstance(exc_instance, APIException):
            notify_to_slack(exc_instance, tb, stack_traces, request.get_full_path())
        return log
