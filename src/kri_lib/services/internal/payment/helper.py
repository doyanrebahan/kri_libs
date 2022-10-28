from urllib.parse import urljoin

from kri_lib.conf import settings
from kri_lib.services.internal.helper import ProxyHelper
from rest_framework.request import Request


class PaymentProxyHelper(ProxyHelper):

    def __init__(self, request: Request, route: str):
        self.request = request
        super(PaymentProxyHelper, self).__init__(request, route, {
            'Authorization': settings.PAYMENT_AUTH_HEADER
        })

    def get_url_proxy(self):
        return urljoin(settings.PAYMENT_SERVICE_URL, self.route)
