from sqlalchemy import func

from datatables import ColumnDT, DataTables

from .helpers import create_dt_params
from .models import Address, User


def get_result(session, column, search_method, search_value):
    columns = [ColumnDT(column, search_method=search_method)]
    query = session.query()
    params = create_dt_params(columns)
    params['columns[0][search][value]'] = search_value
    rowTable = DataTables(params, query, columns)
    return rowTable.output_result()


def test_method_none(session):
    res = get_result(
        session=session,
        column=User.id,
        search_method='none',
        search_value='abc')
    assert res['recordsFiltered'] == '50'


def test_method_numeric(session):
    res = get_result(
        session=session,
        column=User.id,
        search_method='numeric',
        search_value='10')
    assert res['recordsFiltered'] == '1'


def test_method_numeric_illegal_input(session):
    res = get_result(
        session=session,
        column=User.id,
        search_method='numeric',
        search_value='abc')
    try:
        float('abc')
    except ValueError as exc:
        expectedError = str(exc)
    assert expectedError in res['error']


def test_method_numeric_eq(session):
    res = get_result(
        session=session,
        column=User.id,
        search_method='numeric',
        search_value='=10')
    assert res['recordsFiltered'] == '1'


def test_method_numeric_gt(session):
    res = get_result(
        session=session,
        column=User.id,
        search_method='numeric',
        search_value='>10')
    assert res['recordsFiltered'] == '40'


def test_method_numeric_lte(session):
    res = get_result(
        session=session,
        column=User.id,
        search_method='numeric',
        search_value='<=10')
    assert res['recordsFiltered'] == '10'


def test_yadcf_range_number_gt(session):
    res = get_result(
        session=session,
        column=User.id,
        search_method='yadcf_range_number',
        search_value='10-yadcf_delim-')
    assert res['recordsFiltered'] == '41'
    assert res['yadcf_data_0'] == (1, 50)


def test_yadcf_range_number_lt(session):
    res = get_result(
        session=session,
        column=User.id,
        search_method='yadcf_range_number',
        search_value='-yadcf_delim-10')
    assert res['recordsFiltered'] == '10'


def test_yadcf_range_number_range(session):
    res = get_result(
        session=session,
        column=User.id,
        search_method='yadcf_range_number',
        search_value='10-yadcf_delim-15')
    assert res['recordsFiltered'] == '6'


def test_string_contains(session):
    res = get_result(
        session=session,
        column=Address.description,
        search_method='string_contains',
        search_value='street')
    assert res['recordsFiltered'] == '1'


def test_like(session):
    res = get_result(
        session=session,
        column=Address.description,
        search_method='like',
        search_value='%Street%')
    assert res['recordsFiltered'] == '1'


def test_ilike(session):
    res = get_result(
        session=session,
        column=Address.description,
        search_method='ilike',
        search_value='%street%')
    assert res['recordsFiltered'] == '1'


def test_date_lt(session):
    res = get_result(
        session=session,
        column=User.birthday,
        search_method='date',
        search_value='<1970-01-03')
    print(res)
    assert res['recordsFiltered'] == '1'


def test_yadcf_range_date(session):
    res = get_result(
        session=session,
        column=User.birthday,
        search_method='yadcf_range_date',
        search_value='1970-01-03-yadcf_delim-1970-01-13')
    print(res)
    assert res['recordsFiltered'] == '1'


def test_yadcf_autocomplete(session):
    res = get_result(
        session=session,
        column=Address.description,
        search_method='yadcf_autocomplete',
        search_value='Avenue')
    assert set(res['yadcf_data_0']) == set(['Avenue', 'Road', 'Street'])
    assert res['recordsFiltered'] == '1'


def test_yadcf_select(session):
    res = get_result(
        session=session,
        column=Address.description,
        search_method='yadcf_select',
        search_value='Road')
    assert set(res['yadcf_data_0']) == set(['Avenue', 'Road', 'Street'])
    assert res['recordsFiltered'] == '1'


def test_yadcf_multi_select(session):
    res = get_result(
        session=session,
        column=Address.description,
        search_method='yadcf_multi_select',
        search_value='Avenue|StreetRoad')
    assert set(res['yadcf_data_0']) == set(['Avenue', 'Road', 'Street'])
    assert res['recordsFiltered'] == '1'


def test_group_by(session):
    """Test group by after a join query."""
    columns = [ColumnDT(func.count(User.id)), ColumnDT(Address.id)]

    query = session.query().\
        select_from(User).\
        join(Address).\
        group_by(Address)

    params = create_dt_params(columns)
    rowTable = DataTables(params, query, columns)
    res = rowTable.output_result()

    assert len(res['data']) == 3
