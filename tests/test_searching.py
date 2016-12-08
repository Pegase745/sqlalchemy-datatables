"""DataTables unit tests."""
from sqlalchemy import func
from datatables import DataTables, ColumnDT

from . import BaseTest
from .models import User, Address


class SearchingTest(BaseTest):

    """Class defining a test plan for searching elements."""

    def get_result(self, column, search_method, search_value):
        columns = [ColumnDT(column, search_method=search_method)]
        query = self.session.query()
        params = self.create_dt_params(columns)
        params['columns[0][search][value]'] = search_value
        rowTable = DataTables(params, query, columns)
        return rowTable.output_result()

    def test_method_none(self):
        res = self.get_result(
            column=User.id,
            search_method='none',
            search_value='abc')
        assert res['recordsFiltered'] == '50'

    def test_method_numeric(self):
        res = self.get_result(
            column=User.id,
            search_method='numeric',
            search_value='10')
        assert res['recordsFiltered'] == '1'

    def test_method_numeric_illegal_input(self):
        res = self.get_result(
            column=User.id,
            search_method='numeric',
            search_value='abc')
        try:
            float('abc')
        except ValueError as exc:
            expectedError = str(exc)
        assert expectedError in res['error']

    def test_method_numeric_eq(self):
        res = self.get_result(
            column=User.id,
            search_method='numeric',
            search_value='=10')
        assert res['recordsFiltered'] == '1'

    def test_method_numeric_gt(self):
        res = self.get_result(
            column=User.id,
            search_method='numeric',
            search_value='>10')
        assert res['recordsFiltered'] == '40'

    def test_method_numeric_lte(self):
        res = self.get_result(
            column=User.id,
            search_method='numeric',
            search_value='<=10')
        assert res['recordsFiltered'] == '10'

    def test_yadcf_range_number_gt(self):
        res = self.get_result(
            column=User.id,
            search_method='yadcf_range_number',
            search_value='10-yadcf_delim-')
        assert res['recordsFiltered'] == '41'
        assert res['yadcf_data_0'] == (1, 50)

    def test_yadcf_range_number_lt(self):
        res = self.get_result(
            column=User.id,
            search_method='yadcf_range_number',
            search_value='-yadcf_delim-10')
        assert res['recordsFiltered'] == '10'

    def test_yadcf_range_number_range(self):
        res = self.get_result(
            column=User.id,
            search_method='yadcf_range_number',
            search_value='10-yadcf_delim-15')
        assert res['recordsFiltered'] == '6'

    def test_string_contains(self):
        res = self.get_result(
            column=Address.description,
            search_method='string_contains',
            search_value='street')
        assert res['recordsFiltered'] == '1'

    def test_like(self):
        res = self.get_result(
            column=Address.description,
            search_method='like',
            search_value='%Street%')
        assert res['recordsFiltered'] == '1'

    def test_ilike(self):
        res = self.get_result(
            column=Address.description,
            search_method='ilike',
            search_value='%street%')
        assert res['recordsFiltered'] == '1'

    def test_date_lt(self):
        res = self.get_result(
            column=User.birthday,
            search_method='date',
            search_value='<1970-01-03')
        print(res)
        assert res['recordsFiltered'] == '1'

    def test_yadcf_range_date(self):
        res = self.get_result(
            column=User.birthday,
            search_method='yadcf_range_date',
            search_value='1970-01-03-yadcf_delim-1970-01-13')
        print(res)
        assert res['recordsFiltered'] == '1'

    def test_yadcf_autocomplete(self):
        res = self.get_result(
            column=Address.description,
            search_method='yadcf_autocomplete',
            search_value='Avenue')
        assert set(res['yadcf_data_0']) == set(['Avenue', 'Road', 'Street'])
        assert res['recordsFiltered'] == '1'

    def test_yadcf_select(self):
        res = self.get_result(
            column=Address.description,
            search_method='yadcf_select',
            search_value='Road')
        assert set(res['yadcf_data_0']) == set(['Avenue', 'Road', 'Street'])
        assert res['recordsFiltered'] == '1'

    def test_yadcf_multi_select(self):
        res = self.get_result(
            column=Address.description,
            search_method='yadcf_multi_select',
            search_value='Avenue|StreetRoad')
        assert set(res['yadcf_data_0']) == set(['Avenue', 'Road', 'Street'])
        assert res['recordsFiltered'] == '1'


class ComplexQueryTest(BaseTest):

    """Class defining complex query search test plan."""

    def test_group_by(self):
        """Test group by after a join query."""
        columns = [
            ColumnDT(func.count(User.id)),
            ColumnDT(Address.id)]

        query = self.session.query().\
            select_from(User).\
            join(Address).\
            group_by(Address)

        params = self.create_dt_params(columns)
        rowTable = DataTables(params, query, columns)
        res = rowTable.output_result()

        assert len(res['data']) == 3
