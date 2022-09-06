from kri_lib.services.internal.base import BaseInternalServices


class WalletServices(BaseInternalServices):
    dependencies = ('WALLET_SERVICE_URL', 'WALLET_AUTH_HEADER')
