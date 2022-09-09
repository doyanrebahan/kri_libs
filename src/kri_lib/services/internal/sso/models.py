from urllib.parse import urljoin

from kri_lib.conf import settings
from kri_lib.core.models import VirtualModel


class User(VirtualModel):
    first_name: str
    last_name: str
    username: str
    email: str
    phone_number: str
    referral_from: str
    status_kyc: str
    is_active: bool

    def __str__(self):
        return self.email

    def get_request_headers(self) -> dict:
        return {
            'Authorization': settings.SSO_AUTH_HEADER
        }

    def get_url(self):
        return urljoin(
            settings.SSO_SERVICE_URL,
            f'/api/v1/user/detail/{self.unique_id}'
        )

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
