from urllib.parse import urljoin
from uuid import UUID
import requests
from rest_framework import status


class VirtualModel:

    """
    This is for model virtualization, e.g:
    we need data user, and it will return instance
    instead of json / dict

    NOTE: Override this class
    """

    def __init__(self, unique_id):
        if isinstance(unique_id, UUID):
            unique_id = str(unique_id)
        self.unique_id = unique_id
        if unique_id:
            self.bind()

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self}>"

    def __str__(self):
        return self.unique_id

    class DoesNotExist(Exception):
        pass

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
        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise self.DoesNotExist(f'{self.__class__.__name__} matching query does not exist.')

        data = response.json()
        return data

    def bind(self):
        data = self.fetch()
        for key, value in data.items():
            setattr(self, key, value)
