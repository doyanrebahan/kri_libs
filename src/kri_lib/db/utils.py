
from django.utils.functional import empty, LazyObject
from .connection import connection
from .exceptions import UserNotFoundError


class _LazyInstance(LazyObject):

    def _setup(self):
        self._wrapped = empty

    def initialize(self, model, kwargs):
        try:
            instance = model.objects.get(**kwargs)
        except model.DoesNotExist:
            self._wrapped = empty
        except model.MultipleObjectsReturned:
            raise ValueError('arguments required.')
        else:
            self._wrapped = instance

    def set_object(self, instance):
        self._wrapped = instance

    def clear(self):
        self._wrapped = empty


LazyInstance = _LazyInstance()


class LazyInstanceBlock:

    def __init__(self, instance=None, model=None, **kwargs):
        """
        Retrieve LazyObject by instance, or by (model and args)
        """
        self.instance = instance
        self.model = model
        self.kwargs = kwargs
        self._validate_arguments()

    def _validate_arguments(self):
        valid = any([self.instance, self.model])
        if not valid:
            raise ValueError('arguments required.')

    def __enter__(self):
        if self.instance:
            LazyInstance.set_object(self.instance)
        else:
            LazyInstance.initialize(
                self.model,
                self.kwargs.get('kwargs') or self.kwargs
            )

    def __exit__(self, exc_type, exc_val, exc_tb):
        LazyInstance.clear()


def get_user(query: dict) -> dict:
    user = connection['default'].user.find_one(query)  # type: dict
    if not user:
        raise UserNotFoundError(f"Cannot find user with: {query}")
    return user


def get_user_by_uuid(uuid: str) -> dict:
    return get_user(
        query={'user_uuid': uuid}
    )
