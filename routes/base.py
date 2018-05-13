# -*- coding: utf-8 -*-
from functools import wraps


class Route:
    @property
    def name(self):
        return self.__class__.__name__.lower()

    def __str__(self):
        return f'<{self.__module__}.{self.__class__.__name__} url="{self.url}">'

    @classmethod
    def handler(cls, func):

        @wraps(func)
        @classmethod
        def wrap(cls, request):
            return func(request)
        return wrap
