class InternalService:

    SSO = 'SSO'
    WALLET = 'WALLET'
    COMMERCE = 'COMMERCE'
    PAYMENT = 'PAYMENT'
    BACKOFFICE = 'BACKOFFICE'

    @classmethod
    def use(cls, services: list):
        from .conf import ENABLED_SERVICES_CLASSES
        from kri_lib.conf import settings
        from kri_lib.services.internal.sso.conf import SSOServices
        from kri_lib.services.internal.wallet.conf import WalletServices
        from kri_lib.services.internal.commerce.conf import CommerceServices
        from kri_lib.services.internal.payment.conf import PaymentServices
        from kri_lib.services.internal.backoffice.conf import BackofficeServices

        _mapping_class = dict([
            (cls.SSO, SSOServices),
            (cls.WALLET, WalletServices),
            (cls.COMMERCE, CommerceServices),
            (cls.PAYMENT, PaymentServices),
            (cls.BACKOFFICE, BackofficeServices)
        ])
        ENABLED_SERVICES_CLASSES.clear()
        for service in services:
            service_class = _mapping_class.get(service)
            service_class.enabled = True
            ENABLED_SERVICES_CLASSES.append(service_class)
        settings.refresh_proxy()
