from urllib.parse import urljoin

import requests
from kri_lib.conf import settings
from kri_lib.services.internal.helper import ProxyHelper
from rest_framework.request import Request


def get_user_wallets(user_id):
    # fetch addresses
    url = urljoin(
        settings.WALLET_SERVICE_URL,
        f'/api/v1/wallet/addresses/{user_id}'
    )
    response = requests.get(
        url,
        headers={
            'Authorization': settings.WALLET_AUTH_HEADER
        }
    )
    data = response.json()
    return data


class WalletProxyHelper(ProxyHelper):

    def __init__(self, request: Request, route: str):
        super(WalletProxyHelper, self).__init__(request, route, {
            'Authorization': settings.WALLET_AUTH_HEADER
        })

    def get_url_proxy(self):
        return urljoin(settings.WALLET_SERVICE_URL, self.route)
