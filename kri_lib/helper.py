from urllib.parse import urlencode, urljoin, urlparse

import requests
from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from simplejson.scanner import JSONDecodeError


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

    def put(self, payload=None):
        url = self.get_full_path()
        response = requests.put(url, headers=self.headers, data=self.request.POST)
        try:
            data = response.json()
        except JSONDecodeError:
            data = response.text
        self.data = data
        return Response(data, status=response.status_code)

    def post_multipart_form(self, payload=None, files=None):
        url = self.get_full_path()
        request_files = self.request.FILES
        if files:
            request_files = files
        response = requests.post(
            url, headers=self.headers, data=self.request.POST, files=request_files)
        try:
            data = response.json()
        except JSONDecodeError:
            data = response.text
        self.data = data
        return Response(data, status=response.status_code)

    def patch_multipart_form(self, payload=None):
        url = self.get_full_path()
        response = requests.patch(
            url, headers=self.headers, data=self.request.POST, files=self.request.FILES)
        try:
            data = response.json()
        except JSONDecodeError:
            data = response.text
        self.data = data
        return Response(data, status=response.status_code)

    def put_multipart_form(self, payload=None, files=None):
        url = self.get_full_path()
        request_files = self.request.FILES
        if files:
            request_files = files
        response = requests.put(
            url, headers=self.headers, data=self.request.POST, files=request_files)
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


class WalletProxyHelper(ProxyHelper):

    def __init__(self, request: Request, route: str):
        super(WalletProxyHelper, self).__init__(request, route, {
            'Authorization': settings.WALLET_AUTH_HEADER
        })

    def get_url_proxy(self):
        return urljoin(settings.WALLET_SERVICE_URL, self.route)


class StakingProxyHelper(ProxyHelper):

    def __init__(self, request: Request, route: str):
        super(StakingProxyHelper, self).__init__(request, route, {
            'Authorization': settings.STAKING_AUTH_HEADER
        })

    def get_url_proxy(self):
        return urljoin(settings.STAKING_SERVICE_URL, self.route)


class PaymentProxyHelper(ProxyHelper):

    def __init__(self, request: Request, route: str):
        super(PaymentProxyHelper, self).__init__(request, route, {
            'Authorization': settings.PAYMENT_AUTH_HEADER
        })

    def get_url_proxy(self):
        return urljoin(settings.PAYMENT_SERVICE_URL, self.route)


class SSOProxyHelper(ProxyHelper):

    def __init__(self, request: Request, route: str):
        self.request = request
        super(SSOProxyHelper, self).__init__(request, route, {
            'Authorization': settings.SSO_AUTH_HEADER
        })

    def get_url_proxy(self):
        return urljoin(settings.SSO_SERVICE_URL, self.route)


class CommerceProxyHelper(ProxyHelper):

    def __init__(self, request: Request, route: str):
        super(CommerceProxyHelper, self).__init__(request, route, {
            'Authorization': settings.COMMERCE_AUTH_HEADER
        })

    def get_url_proxy(self):
        return urljoin(settings.COMMERCE_SERVICE_URL, self.route)


class CoreProxyHelper(ProxyHelper):

    def __init__(self, request: Request, route: str):
        super(CoreProxyHelper, self).__init__(request, route, {
            'Authorization': settings.CORE_AUTH_HEADER
        })

    def get_url_proxy(self):
        return urljoin(settings.CORE_SERVICE_URL, self.route)


