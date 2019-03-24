import pytest

from datatables import ColumnDT, DataTables

from .helpers import create_dt_params
from .models import Address, User


def test_list(session):
    """Test if it returns a list of users."""
    columns = [ColumnDT(User.id)]

    query = session.query().select_from(User)

    params = create_dt_params(columns)
    rowTable = DataTables(params, query, columns)
    res = rowTable.output_result()

    assert len(res['data']) == 10
    assert len(res['data'][0]) == 1
    assert res['recordsTotal'] == '50'
    assert res['recordsFiltered'] == '50'


def test_list_bad_length(session):
    """Test if it returns an error for querying with a bad length."""
    columns = [ColumnDT(User.id)]

    query = session.query()

    params = create_dt_params(columns, length=-10)
    rowTable = DataTables(params, query, columns)
    res = rowTable.output_result()

    assert 'Length should be' in res['error']


def test_list_detail(session):
    """Test if it returns a list of detailed users."""
    columns = [
        ColumnDT(User.id),
        ColumnDT(User.name),
        ColumnDT(Address.description),
        ColumnDT(User.created_at)
    ]

    query = session.query()

    params = create_dt_params(columns)
    rowTable = DataTables(params, query, columns)
    res = rowTable.output_result()

    assert len(res['data'][0]) == 4


def test_list_fixed_length(session):
    """Test if it returns a fixed list of users."""
    columns = [ColumnDT(User.id)]

    query = session.query()

    params = create_dt_params(columns, length=7)
    rowTable = DataTables(params, query, columns)
    res = rowTable.output_result()

    assert len(res['data']) == 7


def test_list_inner_join(session):
    """Test if it returns a list of users with address."""
    columns = [ColumnDT(User.id)]

    query = session.query().select_from(User).join(Address)

    params = create_dt_params(columns)
    rowTable = DataTables(params, query, columns)
    res = rowTable.output_result()

    assert len(res['data']) == 3
    assert res['recordsTotal'] == '3'
    assert res['recordsFiltered'] == '3'


def test_list_total_length(session):
    """Test if it returns the total list of users."""
    columns = [ColumnDT(User.id)]

    query = session.query()

    params = create_dt_params(columns, length=-1)
    rowTable = DataTables(params, query, columns)
    res = rowTable.output_result()

    assert len(res['data']) == 50


@pytest.fixture(scope="function")
def fixtures_list_hybrid_attributes(session):
    user51 = User(name='User 51')

    session.add(user51)
    session.commit()

    yield

    session.delete(user51)
    session.commit()


@pytest.mark.usefixtures("fixtures_list_hybrid_attributes")
def test_list_hybrid_attributes(session):
    """Test if it returns a list of users with a hybrid property."""
    columns = [
        ColumnDT(User.id),
        ColumnDT(User.dummy),
        ColumnDT(User.name),
        ColumnDT(User.created_at)
    ]

    session.query(*[User.id, User.dummy]).all()

    query = session.query()

    params = create_dt_params(columns, start=50, length=10)
    rowTable = DataTables(params, query, columns)
    res = rowTable.output_result()

    assert len(res['data']) == 1
    assert res['data'][0]['1'] == 'Us'
    assert res['data'][0]['2'] == 'User 51'


@pytest.fixture(scope="function")
def fixtures_list_specific_page(session):
    user51 = User(name='User 51')
    user52 = User(name='User 52')

    session.add(user51)
    session.add(user52)
    session.commit()

    yield

    session.delete(user51)
    session.delete(user52)
    session.commit()


@pytest.mark.usefixtures("fixtures_list_specific_page")
def test_list_specific_page(session):
    """Test if it returns the list of users that are on page 6."""
    columns = [ColumnDT(User.id)]

    query = session.query().select_from(User)

    params = create_dt_params(columns, start=50, length=10)
    rowTable = DataTables(params, query, columns)
    res = rowTable.output_result()

    assert len(res['data']) == 2
    assert res['recordsTotal'] == '52'
    assert res['recordsFiltered'] == '52'
    assert res['data'][0]['0'] == 51
    assert res['data'][1]['0'] == 52
