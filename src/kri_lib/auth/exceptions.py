from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class CrossDomainError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('"You are not authorized to perform this action."')
    default_code = 'authentication_failed'
