from kri_lib.conf import settings
from kri_lib.core import GLOBALS
from kri_lib.logger import generate_api_id
from kri_lib.logger.document import LogRequest
from kri_lib.logger.utils import get_request_body


class BaseKunciLogMiddleware:
    """
    Middleware for initializing API ID.
    """

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
        log = self.record(request)
        response = self.get_response(request)
        log.response_status = response.status_code
        log.save()
        GLOBALS.unset('API_ID')
        response['X-API-ID'] = request.api_id
        # Code to be executed for each request/response after
        # the view is called.

        return response

    def get_api_id(self, request):
        raise NotImplementedError('get_api_id() must be overridden.')

    def record(self, request):
        """
        :param request:
        :return:
        set attr only without saving.
        """
        log = LogRequest()
        log.service_name = settings.LOGGING.get('SERVICE_NAME')
        log.api_id = request.api_id
        log.url = request.get_full_path()
        log.method = request.method
        log.headers = request.headers
        if request.method == 'GET':
            log.payload = request.GET
        else:
            log.payload = get_request_body(request.body)
        return log


class KunciInitLogMiddleware(BaseKunciLogMiddleware):
    """
    Middleware for initializing API_ID.
    """

    def get_api_id(self, request):
        return generate_api_id()


class KunciServiceLogMiddleware(BaseKunciLogMiddleware):
    """
    Middleware for receiving API_ID from API Gateway.
    """

    def get_api_id(self, request):
        return request.headers.get('X-API-ID')
