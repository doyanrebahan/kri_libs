from urllib.parse import urlencode, urlparse

from kri_lib.utils import requests
from rest_framework.request import Request
from rest_framework.response import Response

# json/simplejson module import resolution
try:
    from simplejson import JSONDecodeError
except ImportError:
    from json import JSONDecodeError


class ProxyHelper:
    data = None

    def __init__(self, request: Request, route: str, headers: dict):
        self.request = request
        self.route = route
        self.headers = headers

    def get_url_proxy(self):
        raise NotImplementedError("method get_url_proxy() must be overridden")

    def get_full_path(self):
        url = self.get_url_proxy()
        params = self.request.query_params.dict().copy()
        if params:
            if urlparse(url).query:
                url += '&'
            else:
                url += '?'
            url += urlencode(params)
        return url

    def get(self):
        url = self.get_full_path()
        response = requests.get(url, headers=self.headers)
        try:
            data = response.json()
        except JSONDecodeError:
            data = response.text
        self.data = data
        return Response(data, status=response.status_code)

    def post(self, payload=None):
        url = self.get_full_path()
        response = requests.post(url, headers=self.headers, data=payload)
        try:
            data = response.json()
        except JSONDecodeError:
            data = response.text
        self.data = data
        return Response(data, status=response.status_code)

    def delete(self):
        url = self.get_full_path()
        response = requests.delete(url, headers=self.headers)
        try:
            data = response.json()
        except JSONDecodeError:
            data = response.text
        self.data = data
        return Response(data, status=response.status_code)
