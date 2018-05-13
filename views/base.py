# -*- coding: utf-8 -*-
import tempy.tags as tags
import tempy.widgets as widgets
from models import DBSession
import models.site as site


class NavBar(tags.Nav):
    def __init__(self, request, **kwargs):
        self._request = request
        self._title = self._request.registry.settings.get('site:main').get('site.title')
        super().__init__(**kwargs)

    def init(self):
        self.title = tags.Div(klass='navbar-header')(
            brand=tags.A(klass='navbar-brand mb-0 h1', href='/')(self._title),
            menu_btn=tags.Button(**{
                'type': "button",
                'class': "navbar-toggler",
                'data-toggle': "collapse",
                'data-target': "#navbarSupportedContent",
                'aria-expanded': "false",
                'aria-controls': "navbarSupportedContent",
                'aria-label': "Toggle navigation"
            })(
                tags.Span(klass='navbar-toggler-icon'),
            )
        )
        self.menu = tags.Div(klass='collapse navbar-collapse', id='navbarSupportedContent')
        self._make_menu(self.menu, 'MAIN')
        self(tags.Div(klass='container')(self.title, self.menu))

    def _make_menu(self, container, menu_name):
        menu_items = [
            tags.Li(klass='nav-item')(tags.A(klass='nav-link', href=link.link)(link.name))
            for link in DBSession.query(site.Menu).filter_by(active=True,
                                                             menu=menu_name).order_by(site.Menu.order).all()
        ]
        container(tags.Ul(klass='navbar-nav mr-auto')(menu_items))
        login_link = [[('/login', 'Login'), ], [('/logout', 'Logout'), ]][False]
        user_tags = []
        container(
            tags.Ul(klass='navbar-nav ml-auto navbar-right')(
                user_tags,
                (tags.Li(klass='nav-item')(tags.A(href=link[0], klass='nav-link')(link[1])) for link in login_link)
            )
        )
        return self


class BasePage(widgets.TempyPage):
    def __init__(self, request, **kwargs):
        self._request = request
        super().__init__(**kwargs)

    def js(self):
        return [
            tags.Script(src="https://code.jquery.com/jquery-3.2.1.min.js",
                        integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=",
                        crossorigin="anonymous"),
            tags.Script(src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.3/umd/popper.min.js",
                        integrity="sha384-vFJXuSJphROIrBnz7yo7oB41mKfc8JzQZiCq4NCceLEaO4IHwicKwpJf9c9IpFgh",
                        crossorigin="anonymous"),
            tags.Script(src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js",
                        integrity="sha384-alpBpkh1PFOepccYVYDB4do5UnbKysX5WZXm3XxPqe5iKTfUKjNkCk9SaVuEZflJ",
                        crossorigin="anonymous"),
            tags.Script(defer=True, src="https://use.fontawesome.com/releases/v5.0.0/js/all.js"),
            tags.Script(src=self._request.static_url('app:js/main.js')),
        ]

    @property
    def page_title(self):
        return self._request.registry.settings.get('site:main').get('site.title')

    def css(self):
        return [
            tags.Link(rel="stylesheet", href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css",
                      integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm",
                      crossorigin="anonymous"),
            tags.Link(href="https://fonts.googleapis.com/css?family=Raleway:700|Roboto+Slab", rel="stylesheet"),
            tags.Link(href=self._request.static_url('app:css/style.css'),
                      rel="stylesheet",
                      typ="text/css"),
        ]

    def init(self):
        self.head(self.css(), self.js())
        self.head(tags.Meta(name="viewport", content="width=device-width, initial-scale=1"))
        self.head.title(self.page_title)
        self.navbar = NavBar(self._request, klass='navbar navbar-expand-lg navbar-dark bg-dark fixed-top')
        self.content = tags.Div(klass='container main-window')
        self.footer = tags.Footer(klass='footer footer-dark bg-dark')(
            tags.Div(klass='container')(
                tags.P(klass='text-muted')(
                    "Created by Federico Cerchiari with ",
                    tags.Img(src=self._request.static_url('app:img/brain.png'), height="17px"),
                    ", Python, Pyramid and ",
                    tags.A(href='https://github.com/Hrabal/TemPy')('TemPy'),
                    ". Deployed on AWS Lambda using Zappa. ",
                    tags.A(href='https://github.com/Hrabal/Dobry', target='blank')(
                        'Code on GitHub ',
                        tags.I(klass='fab fa-github')
                    )
                ),
            )
        )
        self.body(
            self.navbar,
            self.content,
            self.footer
        )
