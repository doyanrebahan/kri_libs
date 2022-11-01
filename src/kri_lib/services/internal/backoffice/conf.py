from kri_lib.services.internal.base import BaseInternalServices


class BackofficeServices(BaseInternalServices):
    dependencies = ('BACKOFFICE_SERVICE_URL', 'BACKOFFICE_AUTH_HEADER')
