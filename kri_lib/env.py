import sys
from functools import cached_property
from importlib.machinery import SourceFileLoader
from typing import List, Tuple

from .exceptions import SettingsError

IGNORE_COMMANDS = [
    'check_env'
]


class LocalSettings:

    def __init__(self, path):
        self.path = path
        self.vars = []
        self.errors = []

    @cached_property
    def module(self):
        return SourceFileLoader(
            fullname='local_settings',
            path=self.path
        ).load_module()

    @cached_property
    def module_vars(self):
        return list(
            filter(lambda var: not var.startswith('__'), dir(self.module))
        )

    def _validate_type(self, var_name, value, var_type):
        if not isinstance(value, var_type):
            message = f"{var_name} value should be '{var_type.__name__}'" \
                      f" instead of '{type(value).__name__}'"
            raise ValueError(message)

    def read(self, var, default=None, var_type=str):
        if default is not None:
            self._validate_type("default", default, var_type)
        try:
            value = getattr(self.module, var)
        except AttributeError:
            if default is not None:
                return default
            self.errors.append(f"{var} does not exists in local_settings")
            return None
        self._validate_type(var, value, var_type)
        return value

    def validate(self, var, default=None, var_type=str):
        self.read(var, default, var_type)
        self.vars.append(var)


class Rules:

    def __init__(self, default=None, var_type=str):
        self.var_type = var_type
        self.default = default


class Validate:

    def __init__(self,
                 settings: LocalSettings,
                 rules: List[Tuple[str, Rules]],
                 raise_exception=True):
        self.settings = settings
        self.rules = rules
        self.raise_exception = raise_exception
        self._validate()

    def _must_raise(self):
        if len(sys.argv) == 1 or IGNORE_COMMANDS in sys.argv:
            return False
        return self.raise_exception

    def _validate(self):
        for item in self.rules:
            var, rule = item
            self.settings.validate(
                var=var,
                default=rule.default,
                var_type=rule.var_type
            )
        if self._must_raise() and self.settings.errors:
            raise SettingsError(self.settings.errors)
