from typing import Optional

from django.utils.functional import empty, LazyObject
from .connection import connection
from .exceptions import UserNotFoundError


class KRILazyObject(LazyObject):
    """
    override and define your props.
    """

    def _setup(self):
        self._wrapped = empty

    def set_object(self, instance):
        self._wrapped = instance

    def clear(self):
        self._wrapped = empty


class KRILazySetter:
    lazy_object = None  # type: Optional[KRILazyObject]
    """
    Override this class, and call var LazyObj for get values.

    >>> MyLazyClass(KRILazySetter):
            my_prop: str

    >>> with MyLazyClass(instance=my_instance):
            LazyObj.my_prop
    """

    def __init__(self, instance):
        if self.lazy_object is None:
            raise NotImplementedError(
                f'lazy_object should be overriden '
                f'in class {self.__class__.__name__}'
            )
        self.instance = instance

    def __enter__(self):
        self.lazy_object.set_object(self.instance)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lazy_object.clear()


def get_user(query: dict) -> dict:
    user = connection['default'].user.find_one(query)  # type: dict
    if not user:
        raise UserNotFoundError(f"Cannot find user with: {query}")
    return user


def get_user_by_uuid(uuid: str) -> dict:
    return get_user(
        query={'user_uuid': uuid}
    )
