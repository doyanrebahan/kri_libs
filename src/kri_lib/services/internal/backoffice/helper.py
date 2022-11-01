from urllib.parse import urljoin

from kri_lib.conf import settings
from kri_lib.services.internal.helper import ProxyHelper
from rest_framework.request import Request


class BackofficeProxyHelper(ProxyHelper):

    def __init__(self, request: Request, route: str):
        self.request = request
        super(BackofficeProxyHelper, self).__init__(request, route, {
            'Authorization': settings.BACKOFFICE_AUTH_HEADER
        })

    def get_url_proxy(self):
        return urljoin(settings.BACKOFFICE_SERVICE_URL, self.route)
