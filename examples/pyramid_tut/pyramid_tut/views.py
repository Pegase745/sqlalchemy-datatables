"""Pyramid_tut main views."""
from pyramid.response import Response
from pyramid.view import view_config
from string import upper

from sqlalchemy.exc import DBAPIError

from datatables import ColumnDT, DataTables

from .models import (
    DBSession,
    User,
    Address,
)


@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
    """Try to connect to database, and list available examples."""
    try:
        DBSession.query(User).first()
    except DBAPIError:
        return Response(
            conn_err_msg, content_type='text/plain', status_int=500)
    return {'project': 'pyramid_tut'}


@view_config(route_name='dt_19x', renderer='templates/dt_19x.jinja2')
def dt_19x(request):
    """List users with DataTables <= 1.9.x."""
    return {'project': 'dt_19x'}


@view_config(route_name='dt_110x', renderer='templates/dt_110x.jinja2')
def dt_110x(request):
    """List users with DataTables >= 1.10.x."""
    return {'project': 'dt_110x'}


@view_config(route_name='data', renderer='json')
def data(request):
    """Return server side data."""
    # defining columns
    columns = []
    columns.append(ColumnDT('id'))
    columns.append(ColumnDT('name', filter=upper))
    columns.append(ColumnDT('address.description'))
    columns.append(ColumnDT('created_at'))

    # defining the initial query depending on your purpose
    query = DBSession.query(User).join(Address).filter(Address.id > 14)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.GET, User, query, columns)

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
