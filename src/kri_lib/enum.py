from enum import Enum as DefaultEnum


class Enum(DefaultEnum):

    @classmethod
    def choices(cls):
        if hasattr(cls, '_choices'):
            return cls._choices
        result = [(e.value, e.value) for e in cls]
        cls._choices = result
        return result
