from urllib.parse import urljoin

import requests
from kri_lib.conf import settings


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
