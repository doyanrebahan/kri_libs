from kri_lib.services.internal.base import BaseInternalServices


class SSOServices(BaseInternalServices):
    dependencies = ('SSO_SERVICE_URL', 'SSO_AUTH_HEADER')
