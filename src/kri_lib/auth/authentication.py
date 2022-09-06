import jwt
from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from kri_lib.conf.settings import settings
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from .exceptions import CrossDomainError
from .jwt import jwt_decode_handler


class KRIJWTAuthentication(BaseAuthentication):
    """
    Token based authentication using the JSON Web Token standard.
    """

    def get_jwt_value(self, request):
        auth = get_authorization_header(request).split()
        auth_header_prefix = settings.JWT_AUTH.AUTH_HEADER_PREFIX.lower()

        if not auth:
            return None

        if smart_text(auth[0].lower()) != auth_header_prefix:
            return None

        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        origin = request.headers.get('Origin')
        if payload.get('domain') != origin:
            raise CrossDomainError()

        user = self.authenticate_credentials(payload)

        return user, jwt_value

    def authenticate_credentials(self, payload):
        user = get_user_model()()
        user.user_id = payload.get('user_uuid')
        user.username = payload.get('username')
        user.email = payload.get('email')
        return user
