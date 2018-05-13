# -*- coding: utf-8 -*-
from pyramid.response import Response
from .base import Route


class Home(Route):
    url = '/'

    @Route.handler
    def handler(request):
        return Response('Hello World, <a href="/test" >Test</a>')


class Test(Route):
    url = '/test'

    @Route.handler
    def handler(request):
        return Response('Hello Test!')
