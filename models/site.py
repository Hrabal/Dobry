# -*- coding: utf-8 -*-

from models import Base
from models.dbtools import Dictable
from sqlalchemy import Column, String, Unicode, Integer, Boolean, Float


class Menu(Base, Dictable):
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(64), index=True, unique=True, nullable=False)
    link = Column(String(300), nullable=False)
    active = Column(Boolean(), nullable=False, default=True)
    order = Column(Float(), nullable=False, default=0)
    menu = Column(String(10), default='MAIN')


class Content(Base, Dictable):
    content_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=True)
    text = Column(Unicode())
