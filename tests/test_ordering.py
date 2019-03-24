import pytest

from datatables import ColumnDT, DataTables

from .helpers import create_dt_params
from .models import Address, User


@pytest.fixture(scope="function")
def fixtures_ordering(session):
    """Set up fake population before tests."""
    user51 = User(name='000_User')
    user52 = User(name='zzz_User')
    addr4 = Address(description='000_Address')
    addr5 = Address(description='zzz_Address')
    user53 = User(name='UserFirstAddress', address=addr4)
    user54 = User(name='UserLastAddress', address=addr5)
    session.add(user51)
    session.add(user52)
    session.add(user53)
    session.add(user54)
    session.commit()

    yield

    session.delete(user51)
    session.delete(user52)
    session.delete(user53)
    session.delete(user54)
    session.delete(addr4)
    session.delete(addr5)
    session.commit()


@pytest.mark.usefixtures("fixtures_ordering")
def test_ordering(session):
    """Test if it returns a list with the correct order."""
    columns = [ColumnDT(User.id, ), ColumnDT(User.name)]

    query = session.query().select_from(User)

    # Descending
    params = create_dt_params(columns, order=[{"column": 1, "dir": "desc"}])
    rowTable = DataTables(params, query, columns)
    res = rowTable.output_result()

    assert res['data'][0]['1'] == 'zzz_User'

    # Ascending
    params = create_dt_params(columns, order=[{"column": 1, "dir": "asc"}])

    rowTable = DataTables(params, query, columns)
    res = rowTable.output_result()

    assert res['data'][0]['1'] == '000_User'


@pytest.mark.usefixtures("fixtures_ordering")
def test_ordering_nulls(session):
    """Test if it returns a list with the correct nulls order."""
    columns = [
        ColumnDT(User.id, ),
        ColumnDT(User.name),
        ColumnDT(Address.description, nulls_order='nullsfirst'),
        ColumnDT(User.created_at)
    ]

    query = session.query().select_from(User).join(Address)

    # NULLS FIRST
    params = create_dt_params(columns, order=[{"column": 2, "dir": "desc"}])
    rowTable = DataTables(params, query, columns)
    res = rowTable.output_result()

    if 'error' in res:
        # sqlite3 doesn't support nulls ordering
        assert 'sqlite3.OperationalError) near "NULLS"' in res['error']

    columns = [
        ColumnDT(User.id, ),
        ColumnDT(User.name),
        ColumnDT(Address.description, nulls_order='nullslast'),
        ColumnDT(User.created_at)
    ]

    # NULLS LAST
    params = create_dt_params(columns, order=[{"column": 2, "dir": "asc"}])

    rowTable = DataTables(params, query, columns)
    res = rowTable.output_result()

    if 'error' in res:
        # sqlite3 doesn't support nulls ordering
        assert 'sqlite3.OperationalError) near "NULLS"' in res['error']


@pytest.mark.usefixtures("fixtures_ordering")
def test_ordering_relation(session):
    """Test if it returns a list when ordering a foreign key."""
    columns = [
        ColumnDT(User.id, ),
        ColumnDT(User.name),
        ColumnDT(Address.description),
        ColumnDT(User.created_at)
    ]

    query = session.query().select_from(User).join(Address)

    # Descending
    params = create_dt_params(columns, order=[{"column": 2, "dir": "desc"}])
    rowTable = DataTables(params, query, columns)
    res = rowTable.output_result()

    assert res['data'][0]['1'] == 'UserLastAddress'
    assert res['data'][0]['2'] == 'zzz_Address'

    columns = [
        ColumnDT(User.id, ),
        ColumnDT(User.name),
        ColumnDT(Address.description),
        ColumnDT(User.created_at)
    ]

    # Ascending
    params = create_dt_params(columns, order=[{"column": 2, "dir": "asc"}])

    rowTable = DataTables(params, query, columns)
    res = rowTable.output_result()

    assert res['data'][0]['1'] == 'UserFirstAddress'
    assert res['data'][0]['2'] == '000_Address'
