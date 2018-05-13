# -*- coding: utf-8 -*-
from pyramid.response import Response
from .base import Route

import views.public as v


class Home(Route):
    url = '/'

    @Route.handler
    def handler(request):
        html = v.HomePage(request).render()
        return Response(html)
