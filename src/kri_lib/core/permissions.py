from django.conf import settings
from rest_framework.permissions import AllowAny


class ServiceTokenAuth(AllowAny):

    def has_permission(self, request, view):
        # check if django has attr TESTING with default False value
        if getattr(settings, 'TESTING', False):
            return True
        try:
            prefix, key = request.META.get('HTTP_AUTHORIZATION').split(' ')
        except Exception:
            return False
        else:
            valid_key = (key in settings.SERVICE_TOKEN)
            valid_prefix = (prefix == settings.SERVICE_TOKEN_PREFIX)
            return all([valid_key, valid_prefix])
