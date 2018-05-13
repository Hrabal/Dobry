# -*- coding: utf-8 -*-
import os
import importlib
from .base import Route


def isRoute(obj):
    try:
        issubclass(obj, object)
    except TypeError:
        return False
    else:
        return issubclass(x, Route) and x is not Route


module_path = os.path.dirname(os.path.abspath(__file__))
route_files = [f for f in os.listdir(module_path) if f.endswith('.py') and f not in ('__init__.py', 'base.py')]
routes = []
for f in route_files:
    m_path = os.path.join(module_path, f)
    module = importlib.import_module(f'routes.{f[:-3]}')
    for c in dir(module):
        x = getattr(module, c)
        if isRoute(x):
            routes.append(x)
__all__ = routes
