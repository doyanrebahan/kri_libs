from kri_lib.services.internal.base import BaseInternalServices


class PaymentServices(BaseInternalServices):
    dependencies = ('PAYMENT_SERVICE_URL', 'PAYMENT_AUTH_HEADER')
