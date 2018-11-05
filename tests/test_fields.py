import pytest
from sqlalchemy import func

from datatables import ColumnDT, DataTables

from .helpers import create_dt_params
from .models import Address, User


def test_fields_mdata(session):
    """Test if the result's data have mData set."""
    columns = [
        ColumnDT(User.id, mData='ID'),
        ColumnDT(User.name, mData='Username'),
        ColumnDT(Address.description, mData='Address'),
        ColumnDT(User.created_at, mData='Created at')
    ]

    query = session.query().select_from(User).join(Address)

    params = create_dt_params(columns)
    rowTable = DataTables(params, query, columns)
    res = rowTable.output_result()

    assert len(res['data']) == 3
    assert 'ID' in res['data'][0]
    assert 'Username' in res['data'][0]
    assert 'Address' in res['data'][0]
    assert 'Created at' in res['data'][0]


def test_fields_search_filters(session):
    """Test if the result's data are filtered after search."""
    query = session.query()

    columns = [
        ColumnDT(User.id, search_method='numeric'),
        ColumnDT(User.name, search_method='string_contains'),
        ColumnDT(User.birthday, search_method='date')
    ]

    user = session.query(User).filter(User.id == 4).one()

    params = create_dt_params(columns)
    params['columns[0][search][value]'] = '=4'
    params['columns[1][search][value]'] = user.name
    params['columns[2][search][value]'] = '>1965-02-02'
    params['columns[2][search][value]'] = '<=99'
    rowTable = DataTables(params, query, columns)
    res = rowTable.output_result()

    assert len(res['data']) == 1


def test_calculating_age_on_the_fly(session):
    """Test if the result's have a custom field."""
    query = session.query().filter(User.id > 5)

    columns = [
        ColumnDT(User.id, search_method='numeric'),
        ColumnDT(User.name, search_method='string_contains'),
        ColumnDT(User.birthday, search_method='date'),
        ColumnDT(func.datetime('now') - User.birthday, search_method='numeric')
    ]

    params = create_dt_params(columns)
    rowTable = DataTables(params, query, columns)
    res = rowTable.output_result()

    assert len(res['data']) == 10


@pytest.fixture(scope="function")
def fixtures_filed_filtering(session):
    user51 = User(name='User 51')
    user52 = User(name='User 52')

    session.add(user51)
    session.add(user52)
    session.commit()

    yield

    session.delete(user51)
    session.delete(user52)
    session.commit()


@pytest.mark.usefixtures("fixtures_filed_filtering")
def test_fields_filtering(session):
    """Test if result's are filtered from global search field."""
    columns = [ColumnDT(User.id, ), ColumnDT(User.name)]

    query = session.query().select_from(User)

    params = create_dt_params(columns, search='51')
    rowTable = DataTables(params, query, columns)
    res = rowTable.output_result()

    assert len(res['data']) == 1
    assert res['recordsTotal'] == '52'
    assert res['recordsFiltered'] == '1'
    assert res['data'][0]['1'] == 'User 51'


@pytest.fixture(scope="function")
def fixtures_fields_global_search_filtering_with_regex(session):
    user51 = User(name='Run To')
    user52 = User(name='Feeeeear Of')

    session.add(user51)
    session.add(user52)
    session.commit()

    yield

    session.delete(user51)
    session.delete(user52)
    session.commit()


@pytest.mark.usefixtures("fixtures_fields_global_search_filtering_with_regex")
def test_fields_global_search_filtering_with_regex(session):
    """Test if result's are filtered from global search field."""
    columns = [ColumnDT(User.id, ), ColumnDT(User.name)]

    query = session.query().select_from(User)

    params = create_dt_params(columns, search='Fe*ar')
    params['search[regex]'] = 'true'

    rowTable = DataTables(params, query, columns, allow_regex_searches=True)
    res = rowTable.output_result()

    if 'error' in res:
        # unfortunately sqlite doesn't support regexp out of the box'
        assert 'no such function: REGEXP' in res['error']
    else:
        assert len(res['data']) == 1
        assert res['recordsTotal'] == '1'
        assert res['recordsFiltered'] == '1'
        assert res['data'][0]['1'] == 'Feeeeear Of'


@pytest.fixture(scope="function")
def fixtures_column_not_searchable(session):
    user51 = User(name='User 51')

    session.add(user51)
    session.commit()

    yield

    session.delete(user51)
    session.commit()


@pytest.mark.usefixtures("fixtures_column_not_searchable")
def test_column_not_searchable(session):
    """Test if result's are filtered from global search field."""
    columns = [
        ColumnDT(User.id, mData='ID'),
        ColumnDT(User.name, mData='Username', global_search=False)
    ]

    query = session.query().select_from(User)

    params = create_dt_params(columns, search='User 51')
    rowTable = DataTables(params, query, columns)
    res = rowTable.output_result()

    assert len(res['data']) == 0
    assert res['recordsTotal'] == '51'
    assert res['recordsFiltered'] == '0'
