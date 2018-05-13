# -*- coding: utf-8 -*-
import os
from configparser import ConfigParser
from pyramid.config import Configurator

from wsgiref.simple_server import make_server

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

import routes
from models import initialize_sql


def db_session_maker(request):
    maker = request.registry.dbmaker
    session = maker()

    def cleanup(request):
        if request.exception is not None:
            session.rollback()
        else:
            session.commit()
        session.close()
    request.add_finished_callback(cleanup)

    return session


def db_uri_from_env(settings):
    user, pwd = os.environ['DB_USR'], os.environ['DB_PWD']
    naked_uri = settings['db:main'].get('db.naked_uri')
    db_name = settings['db:main'].get('db.db_name')
    engine_type = settings['db:main'].get('db.engine')
    settings.set('db:main', 'sqlalchemy.url', f'{engine_type}://{user}:{pwd}@{naked_uri}/{db_name}')


def make_wsgi_app(**kwargs):
    # Settings inheritance: env ini overrides default ini
    env = kwargs.pop('env')
    env_settings_file = f'{env}.ini'
    settings = ConfigParser()
    settings.read('default.ini')
    settings.read(env_settings_file)

    with Configurator(settings=settings) as config:
        # Db configuration
        # config.scan('models')
        db_uri_from_env(settings)
        engine = engine_from_config(settings['db:main'])
        initialize_sql(engine)
        config.registry.dbmaker = sessionmaker(bind=engine)
        config.add_request_method(db_session_maker, reify=True)
        print('Connected to Db', engine)

        # Dynamic routes handling
        routes_l = [route_cls() for route_cls in routes.__all__]
        for route in routes_l:
            config.add_route(route.name, route.url)
            config.add_view(route.handler, route_name=route.name)
        print('Imported routes: %s' % ', '.join(str(r) for r in routes_l) if routes_l else 'Empty /routes directory.')

        # Static assets views
        setup = config.get_settings()
        for asset_type, uri in setup.get('assets:main').items():
            config.add_static_view(path=f'app:{asset_type}', name=uri)

        return config.make_wsgi_app()


def zappa_wsgi_app(app, environ):
    wsgi_app = make_wsgi_app()
    return wsgi_app(app, environ)


if __name__ == '__main__':
    env = 'localhost'
    app = make_wsgi_app(env=env)
    host = app.registry.settings.get('server:main').get('host')
    port = app.registry.settings.get('server:main').getint('port')
    server = make_server(host, port, app)
    print(f'Serving on {host}:{port}')
    server.serve_forever()
