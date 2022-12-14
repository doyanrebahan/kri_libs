from datetime import datetime
from urllib.parse import urljoin

import requests
from kri_lib.conf import settings
from kri_lib.core import GLOBALS
from kri_lib.logger import generate_api_id
from kri_lib.logger.document import LogRequest
from kri_lib.logger.utils import get_request_body, to_preserve


class BaseKunciLogMiddleware:

    SAFE_KEY_HEADER = ['Authorization']
    SAFE_KEY_BODY = ['password']

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.api_id = self.get_api_id(request)

        if not request.api_id:
            return self.get_response(request)

        GLOBALS.set('API_ID', request.api_id)
        log_payload = self.prepare_save(request)
        response = self.get_response(request)
        log_payload['response_status'] = response.status_code
        self.record(payload=log_payload)
        GLOBALS.unset('API_ID')
        response['X-API-ID'] = request.api_id
        # Code to be executed for each request/response after
        # the view is called.
        return response

    def get_api_id(self, request) -> str:
        raise NotImplementedError('get_api_id() must be overridden.')

    def prepare_save(self, request) -> dict:
        if request.method == 'GET':
            payload = request.GET
        else:
            body = get_request_body(request)
            payload = to_preserve(body.copy(), self.SAFE_KEY_BODY)
        return {
            'service_name': settings.LOGGING.get('SERVICE_NAME'),
            'api_id': request.api_id,
            'url': request.get_full_path(),
            'method': request.method,
            'headers': to_preserve(
                dict(request.headers.copy()),
                self.SAFE_KEY_HEADER
            ),
            'payload': payload,
            'timestamp': datetime.now()
        }

    def record(self, payload):
        raise NotImplementedError


class BaseKunciLogAPIMiddleware(BaseKunciLogMiddleware):

    def record(self, payload):
        url = urljoin(
            settings.LOGGING.get('API').get('host'),
            '/api/v1/log/log-request'
        )
        payload['timestamp'] = str(payload['timestamp'])
        response = requests.post(
            url=url,
            json=payload,
            headers={
                'Authorization': settings.LOGGING.get('API').get('Authorization')
            }
        )
        return response


class KunciInitLogAPIMiddleware(BaseKunciLogAPIMiddleware):
    """
    Middleware for initializing API_ID.
    """

    def get_api_id(self, request):
        return generate_api_id()


class KunciServiceLogAPIMiddleware(BaseKunciLogAPIMiddleware):
    """
    Middleware for receiving API_ID from API Gateway.
    """

    def get_api_id(self, request):
        return request.headers.get('X-API-ID')


class KunciMultiLogAPIMiddleware(BaseKunciLogAPIMiddleware):
    """
    Middleware for initializing API_ID
    or receiving API_ID from API Gateway.
    """

    def get_api_id(self, request):
        api_id = request.headers.get('X-API-ID')
        if not api_id:
            return generate_api_id()
        return api_id


class BaseKunciLogDBMiddleware(BaseKunciLogMiddleware):

    def record(self, payload):
        """
        :param request:
        :return:
        set attr only without saving.
        """
        log = LogRequest()
        for key, value in payload.items():
            setattr(log, key, value)
        return log


class KunciInitLogMiddleware(BaseKunciLogDBMiddleware):
    """
    Middleware for initializing API_ID.
    """

    def get_api_id(self, request):
        return generate_api_id()


class KunciServiceLogMiddleware(BaseKunciLogDBMiddleware):
    """
    Middleware for receiving API_ID from API Gateway.
    """

    def get_api_id(self, request):
        return request.headers.get('X-API-ID')


class KunciMultiLogMiddleware(BaseKunciLogDBMiddleware):
    """
    Middleware for initializing API_ID
    or receiving API_ID from API Gateway.
    """

    def get_api_id(self, request):
        api_id = request.headers.get('X-API-ID')
        if not api_id:
            return generate_api_id()
        return api_id
