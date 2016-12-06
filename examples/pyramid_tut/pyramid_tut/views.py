"""Pyramid_tut main views."""
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from sqlalchemy import func
from datatables import ColumnDT, DataTables

from .models import Address, DBSession, User


@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
    """Try to connect to database, and list available examples."""
    try:
        DBSession.query(User).first()
    except DBAPIError:
        return Response(
            conn_err_msg, content_type='text/plain', status_int=500)
    return {'project': 'pyramid_tut'}


@view_config(route_name='dt_110x', renderer='templates/dt_110x.jinja2')
def dt_110x(request):
    """List users with DataTables >= 1.10.x."""
    return {'project': 'dt_110x'}


@view_config(route_name='dt_110x_basic_column_search',
             renderer='templates/dt_110x_basic_column_search.jinja2')
def dt_110x_basic_column_search(request):
    """Text based per column search"""
    return {'project': 'dt_110x_basic_column_search'}


@view_config(route_name='dt_110x_advanced_column_search',
             renderer='templates/dt_110x_advanced_column_search.jinja2')
def dt_110x_advanced_column_search(request):
    """Advanced per column search"""
    return {'project': 'dt_110x_advanced_column_search'}


@view_config(route_name='dt_110x_yadcf',
             renderer='templates/dt_110x_yadcf.jinja2')
def dt_110x_yadcf(request):
    """Search with yadcf"""
    return {'project': 'dt_110x_yadcf'}


@view_config(route_name='data', renderer='json')
def data(request):
    """Return server side data."""
    # defining columns
    # explicilty cast date to string, so string searching the date
    # will give search a date formatted equal to how it is presented
    columns = [
        ColumnDT(User.id),
        ColumnDT(User.name),
        ColumnDT(Address.description),
        ColumnDT(func.strftime('%d-%m-%Y', User.birthday)),
        ColumnDT(User.age)
    ]

    # defining the initial query depending on your purpose
    query = DBSession.query().\
        select_from(User).\
        join(Address).\
        filter(Address.id > 4)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.GET, query, columns)

    # returns what is needed by DataTable
    return rowTable.output_result()


@view_config(route_name='data_advanced', renderer='json_with_dates')
def data_advanced(request):
    """Return server side data."""
    # defining columns
    columns = [
        ColumnDT(User.id, search_method='numeric'),
        ColumnDT(User.name),
        ColumnDT(Address.description),
        ColumnDT(User.birthday, search_method='date'),
        ColumnDT(User.age, search_method='numeric')
    ]

    # defining the initial query depending on your purpose
    query = DBSession.query().\
        select_from(User).\
        join(Address).\
        filter(Address.id > 4)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.GET, query, columns)

    # returns what is needed by DataTable
    return rowTable.output_result()


@view_config(route_name='data_yadcf', renderer='json_with_dates')
def data_yadcf(request):
    """Return server side data."""
    # defining columns
    columns = [
        ColumnDT(User.id, search_method='yadcf_range_number'),
        ColumnDT(User.name, search_method='yadcf_multi_select'),
        ColumnDT(Address.description, search_method='yadcf_autocomplete'),
        ColumnDT(User.birthday, search_method='yadcf_range_date'),
        ColumnDT(User.age, search_method='yadcf_range_number_slider')
    ]

    # defining the initial query depending on your purpose
    query = DBSession.query().\
        select_from(User).\
        join(Address).\
        filter(Address.id > 4)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.GET, query, columns)

    # returns what is needed by DataTable
    return rowTable.output_result()


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_pyramid_tut_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
