from urllib.parse import urljoin
from kri_lib.conf import settings
from kri_lib.core.serializers import ProxySerializer


class WalletProxySerializer(ProxySerializer):

    def get_proxy_host(self):
        return settings.WALLET_SERVICE_URL

    def get_url_proxy(self) -> str:
        return urljoin(self.get_proxy_host(), self.get_proxy_route())

    def get_request_headers(self) -> dict:
        return {
            'Authorization': settings.WALLET_AUTH_HEADER
        }
