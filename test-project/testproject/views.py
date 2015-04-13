from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    User,
    Address,
)

from datatables import ColumnDT, DataTables


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_test-project_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""


def _upper(chain):
    ret = chain.upper()
    if ret:
        return ret
    else:
        return chain


@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    try:
        DBSession.query(User).first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'project': 'test-project'}


@view_config(route_name='simple_example', request_method='GET', renderer='json')
def simple_example(request):
    # defining columns
    columns = []
    columns.append(ColumnDT('id'))
    columns.append(ColumnDT('name', filter=_upper))
    columns.append(ColumnDT('address.description'))
    columns.append(ColumnDT('created_at'))

    # defining the initial query depending on your purpose
    query = DBSession.query(User).join(Address).filter(Address.id > 14)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request, User, query, columns)

    # returns what is needed by DataTable
    return rowTable.output_result()


@view_config(route_name='relation_example', request_method='GET', renderer='json')
def relation_example(request):
    pass
