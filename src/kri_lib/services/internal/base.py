from kri_lib.conf.exceptions import SettingsError


class BaseInternalServices:
    enabled = False
    dependencies = tuple()

    @classmethod
    def validate_dependencies(cls, settings):
        for var in cls.dependencies:
            value = getattr(settings, var)
            if not isinstance(value, bool) and not value:
                raise SettingsError(f'{var} is required for using {cls.__class__.__name__}')
