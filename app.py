# -*- coding: utf-8 -*-
from wsgiref.simple_server import make_server

from pyramid.response import Response
from pyramid.config import Configurator
from configparser import ConfigParser
import routes


def hello_world(request):
    return Response('Hello world simple func!')


def make_wsgi_app(env, **vars):
    parser = ConfigParser()
    parser.read(f'{env}.ini')
    settings = dict(parser.items('app:main', vars=vars))
    with Configurator(**settings) as config:
        routes_l = [route_cls() for route_cls in routes.__all__]
        for route in routes_l:
            config.add_route(route.name, route.url)
            config.add_view(route.handler, route_name=route.name)
        print('Imported routes: %s' % ', '.join(str(r) for r in routes_l) if routes_l else 'Empty /routes directory.')
        return config.make_wsgi_app(), parser


def zappa_wsgi_app(app, environ):
    wsgi_app = make_wsgi_app()
    return wsgi_app(app, environ)


if __name__ == '__main__':
    env = 'localhost'
    app, server_settings = make_wsgi_app(env)
    server = make_server(server_settings.get('server:main', 'host'),
                         server_settings.getint('server:main', 'port'),
                         app)
    server.serve_forever()
