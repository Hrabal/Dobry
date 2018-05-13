# -*- coding: utf-8 -*-
from .base import BasePage


class HomePage(BasePage):
    def init(self):
        self.content('CIAO')
