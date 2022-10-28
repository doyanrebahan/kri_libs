from kri_lib.services.internal.base import BaseInternalServices


class CommerceServices(BaseInternalServices):
    dependencies = ('COMMERCE_SERVICE_URL', 'COMMERCE_AUTH_HEADER')
