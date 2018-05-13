# -*- coding: utf-8 -*-
from wsgiref.simple_server import make_server

from pyramid.response import Response
from pyramid.config import Configurator
import routes


def hello_world(request):
    return Response('Hello world simple func!')


def make_wsgi_app():
    with Configurator() as config:
        routes_l = [route_cls() for route_cls in routes.__all__]
        for route in routes_l:
            config.add_route(route.name, route.url)
            config.add_view(route.handler, route_name=route.name)
        print('Imported routes: %s' % ', '.join(str(r) for r in routes_l) if routes_l else 'Empty /routes directory.')
        return config.make_wsgi_app()


def zappa_wsgi_app(app, environ):
    wsgi_app = make_wsgi_app()
    return wsgi_app(app, environ)


if __name__ == '__main__':
    app = make_wsgi_app()
    server = make_server('localhost', 4443, app)
    server.serve_forever()
