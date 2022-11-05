
from django.utils.functional import empty, LazyObject
from .connection import connection
from .exceptions import UserNotFoundError


class BaseLazyObject(LazyObject):

    def _setup(self):
        self._wrapped = empty

    def get_field_object(self, instance, fields):
        payload = {}
        for field in fields:
            payload[field] = getattr(instance, field)
        return payload

    def set_object(self, instance, fields):
        self._wrapped = self.get_field_object(instance, fields)

    def clear(self):
        self._wrapped = empty


class BaseLazyInstance:

    lazy_object = BaseLazyObject()

    def __init__(self, instance=None):
        self.instance = instance

    def __enter__(self):
        self.lazy_object.set_object(self.instance, self.fields)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lazy_object.clear()

    @property
    def fields(self):
        raise NotImplementedError('fields must be overridden.')


def get_user(query: dict) -> dict:
    user = connection['default'].user.find_one(query)  # type: dict
    if not user:
        raise UserNotFoundError(f"Cannot find user with: {query}")
    return user


def get_user_by_uuid(uuid: str) -> dict:
    return get_user(
        query={'user_uuid': uuid}
    )
