from urllib.parse import urljoin
import requests

from kri_lib.conf import settings


class VirtualModel:

    """
    This is for model virtualization, e.g:
    we need data user, and it will return instance
    instead of json / dict

    NOTE: Override this class
    """

    def __init__(self, unique_id):
        self.unique_id = unique_id
        if unique_id:
            self.bind()

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self}>"

    def __str__(self):
        return self.unique_id

    def get_url(self):
        """
        Override this method
        """
        raise NotImplementedError("method get_url() must be overridden.")

    def get_request_headers(self) -> dict:
        raise NotImplementedError("method get_request_headers() must be overridden.")

    def fetch(self) -> dict:
        path = urljoin(self.get_url(), self.unique_id)
        response = requests.get(
            url=path,
            headers=self.get_request_headers()
        )
        data = response.json()
        return data

    def bind(self):
        data = self.fetch()
        for key, value in data.items():
            setattr(self, key, value)


class User(VirtualModel):
    first_name: str
    last_name: str
    username: str
    email: str
    phone_number: str
    referral_from: str
    status_kyc: str

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
