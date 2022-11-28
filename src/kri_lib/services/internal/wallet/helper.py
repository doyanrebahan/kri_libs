from urllib.parse import urljoin

import requests
from kri_lib.conf import settings
from kri_lib.logger.utils import db_print
from kri_lib.services.internal.helper import ProxyHelper
from rest_framework.exceptions import APIException
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
    if response.ok:
        return response.json()
    db_print(response.text)
    raise APIException({'wallet': 'could not fetch wallet address.'})


def get_user_wallet(user_id, wallet_type):
    addresses = get_user_wallets(user_id)
    if not addresses:
        raise NotImplementedError('wallet address does not exists.')
    try:
        return list(
            filter(lambda wallet: wallet.get('wallet_type') == wallet_type, addresses)
        )[0]
    except IndexError:
        raise APIException(addresses)


class WalletProxyHelper(ProxyHelper):

    def __init__(self, request: Request, route: str):
        super(WalletProxyHelper, self).__init__(request, route, {
            'Authorization': settings.WALLET_AUTH_HEADER
        })

    def get_url_proxy(self):
        return urljoin(settings.WALLET_SERVICE_URL, self.route)
