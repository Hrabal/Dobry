# -*- coding: utf-8 -*-
import os
import importlib
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker


class CustomBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=CustomBase)
DBSession = scoped_session(sessionmaker())


def isModel(obj):
    try:
        issubclass(obj, object)
    except TypeError:
        return False
    else:
        return issubclass(x, Base) and x is not Base


module_path = os.path.dirname(os.path.abspath(__file__))
model_files = [f for f in os.listdir(module_path) if f.endswith('.py') and f not in ('__init__.py', 'base.py')]
models = []
for f in model_files:
    m_path = os.path.join(module_path, f)
    module = importlib.import_module(f'models.{f[:-3]}')
    for c in dir(module):
        x = getattr(module, c)
        if isModel(x):
            models.append(x)
__all__ = models

print('Imported models: %s' % ', '.join(str(m) for m in models) if models else 'No models avaiable in the models directory.')


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
