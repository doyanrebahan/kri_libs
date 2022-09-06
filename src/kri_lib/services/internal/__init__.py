class InternalService:

    SSO = 'SSO'
    WALLET = 'WALLET'

    @classmethod
    def use(cls, services: list):
        from .conf import ENABLED_SERVICES_CLASSES
        from kri_lib.conf import settings
        from kri_lib.services.internal.sso.conf import SSOServices
        from kri_lib.services.internal.wallet.conf import WalletServices

        _mapping_class = dict([
            (cls.SSO, SSOServices),
            (cls.WALLET, WalletServices)
        ])
        ENABLED_SERVICES_CLASSES.clear()
        for service in services:
            service_class = _mapping_class.get(service)
            service_class.enabled = True
            ENABLED_SERVICES_CLASSES.append(service_class)
        settings.refresh_proxy()
