from datetime import date

from pyramid.config import Configurator
from pyramid.renderers import JSON
from sqlalchemy import engine_from_config

from .models import Base, DBSession


def date_adapter(obj, request):
    return str(obj)


def main(global_config, **settings):
    """Return a Pyramid WSGI application."""
    engine = engine_from_config(settings, "sqlalchemy.")

    DBSession.configure(bind=engine)

    Base.metadata.bind = engine

    config = Configurator(settings=settings)

    config.include("pyramid_jinja2")

    config.include("pyramid_debugtoolbar")

    config.add_route("home", "/")

    config.add_route("data", "/data")

    config.add_route("data_advanced", "/data_advanced")

    config.add_route("data_yadcf", "/data_yadcf")

    config.add_route("dt_110x", "/dt_110x")

    config.add_route("dt_110x_custom_column", "/dt_110x_custom_column")

    config.add_route("dt_110x_basic_column_search", "/dt_110x_basic_column_search")

    config.add_route(
        "dt_110x_advanced_column_search", "/dt_110x_advanced_column_search"
    )

    config.add_route("dt_110x_yadcf", "/dt_110x_yadcf")

    config.scan()

    json_renderer = JSON()

    json_renderer.add_adapter(date, date_adapter)

    config.add_renderer("json_with_dates", json_renderer)

    config.add_jinja2_renderer(".html")

    return config.make_wsgi_app()
