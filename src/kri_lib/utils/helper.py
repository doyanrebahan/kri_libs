import traceback
from json.decoder import JSONDecodeError
from urllib.parse import urljoin

import requests
from django.conf import settings
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.status import is_client_error


class RequestHelper:

    def __init__(self, host=None):

        self.host = host
        self.response = None

    @property
    def service_mapping(self):
        return [
           {
                "host": settings.SSO_SERVICE_URL,
                "headers": {
                    "Authorization": settings.SSO_AUTH_HEADER
                }
            }, {
                "host": settings.PAYMENT_SERVICE_URL,
                "headers": {
                    "Authorization": settings.PAYMENT_AUTH_HEADER
                }
            }, {
                "host": settings.COMMERCE_SERVICE_URL,
                "headers": {
                    "Authorization": settings.COMMERCE_AUTH_HEADER
                }
            }, {
                "host": settings.WALLET_SERVICE_URL,
                "headers": {
                    "Authorization": settings.WALLET_AUTH_HEADER
                }
            },
        ]

    @property
    def request_headers(self):
        for service in self.service_mapping:
            try:
                if service.get('host') == self.host:
                    return service.get('headers')
            except AttributeError:
                pass
        return {}

    def get_url(self, route):
        return urljoin(self.host, route)

    def server_error_message(self, url):
        message = f"An error occurred while requesting to {url}"
        return {
            "message": message
        }

    def handle_response_error(self, response):
        if is_client_error(response.status_code):
            if response.status_code == 400:
                messages = response.json()
                if isinstance(messages, dict):
                    for key, value in messages.items():
                        raise ValidationError({
                            key: value
                        })
            raise ValidationError(response.text)
        raise APIException(response.text)

    def get_json(self):
        try:
            return self.response.json()
        except JSONDecodeError:
            return self.response.text

    def do_response(self, response):
        if not response.ok:
            return self.handle_response_error(response)
        return response

    def _request(self, method, **kwargs):
        if not kwargs.get('headers'):
            kwargs.update({
                'headers': self.request_headers
            })
        try:
            response = requests.request(method=method, **kwargs)
        except requests.exceptions.ConnectionError:
            print(traceback.format_exc())
            raise APIException(
                self.server_error_message(kwargs.get('url'))
            )
        self.response = response
        return self.do_response(response)

    def request(self, method, route=None, **kwargs):
        if route:
            kwargs.update({
                'url': self.get_url(route)
            })
        return self._request(
            method,
            **kwargs
        )

    def get(self, route=None, **kwargs):
        return self._request(
            method="get",
            route=route,
            **kwargs
        )

    def post(self, route=None, **kwargs):
        return self._request(
            method="post",
            route=route,
            **kwargs
        )

