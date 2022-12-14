from datetime import timedelta

from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
from django.core.signals import setting_changed


DEFAULT = {
    'JWT_AUTH': {
        'AUTH_HEADER_PREFIX': '',
        'SECRET_KEY': '',
        'JWT_EXPIRATION_DELTA': timedelta(seconds=300),
        'JWT_ALGORITHM': 'HS256',
        'JWT_VERIFY_EXPIRATION': True,
        'ALLOW_REFRESH': True,
        'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7)
    },
    'DATABASES': {
        'default': ''
    },
    'LOGGING': {
        'SERVICE_NAME': '',
        'DATABASE': '',
        'API': {
            'host': '',
            'Authorization': ''
        },
        'SLACK': {
            'HOOKS_URL': ''
        }
    }
}

try:
    USER_SETTINGS = getattr(django_settings, 'KRI_LIB', {})
except ImproperlyConfigured:
    USER_SETTINGS = {}

# We will centralize settings, so just proxy from settings object
# or whatever is that. but the final result is proxy this attrs.
PROXY_SETTINGS = []


class _BaseSettings:
    def __init__(self, default, user_settings, proxy=None):
        self.default = default
        self.user_settings = user_settings
        self._proxy = proxy

    def __getattr__(self, item):
        if self._proxy and item in PROXY_SETTINGS:
            return getattr(self._proxy, item)

        if item not in self.default:
            raise AttributeError(f"Invalid Lib settings: {item}")
        try:
            return self.user_settings[item]
        except KeyError:
            return self.default[item]


class _ProxySettings:

    def __init__(self, proxy, proxy_settings):
        self.proxy = proxy
        self.proxy_settings = proxy_settings
        self._bind()

    def _bind(self):
        for item in self.proxy_settings:
            value = getattr(self.proxy, item)
            setattr(self, item, value)


def _proxy_from_django_settings():
    from kri_lib.services.internal.conf import ENABLED_SERVICES_CLASSES

    for services in ENABLED_SERVICES_CLASSES:
        services.validate_dependencies(django_settings)
        PROXY_SETTINGS.extend(services.dependencies)

    proxy_settings = _ProxySettings(
        proxy=django_settings,
        proxy_settings=PROXY_SETTINGS
    )
    return proxy_settings


class JWTSettings(_BaseSettings):
    pass


class LibSettings(_BaseSettings):
    JWT_AUTH = JWTSettings(
        default=DEFAULT.get('JWT_AUTH'),
        user_settings=USER_SETTINGS.get('JWT_AUTH', {})
    )

    def __init__(self, **kwargs):
        super(LibSettings, self).__init__(
            default=DEFAULT,
            user_settings=USER_SETTINGS,
            **kwargs
        )

    def refresh_proxy(self):
        self._proxy = _proxy_from_django_settings()


settings = LibSettings(proxy=_proxy_from_django_settings())


def reload_proxy_settings(*args, **kwargs):
    PROXY_SETTINGS.clear()
    settings.refresh_proxy()


setting_changed.connect(reload_proxy_settings)
