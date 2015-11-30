"""Initialize application."""
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """Return a Pyramid WSGI application."""
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_route('home', '/')
    config.add_route('data', '/data')
    config.add_route('dt_19x', '/dt_19x')
    config.add_route('dt_110x', '/dt_110x')
    config.scan()
    return config.make_wsgi_app()
