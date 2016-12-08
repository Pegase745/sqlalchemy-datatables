"""Column DataTable unit tests."""
from sqlalchemy import func
from datatables import DataTables, ColumnDT

from . import BaseTest
from .models import User, Address


class FieldsTest(BaseTest):

    """Class defining a test plan for fields."""

    def test_fields_mdata(self):
        """Test if the result's data have mData set."""
        columns = [
            ColumnDT(User.id, mData='ID'),
            ColumnDT(User.name, mData='Username'),
            ColumnDT(Address.description, mData='Address'),
            ColumnDT(User.created_at, mData='Created at')]

        query = self.session.query().select_from(User).join(Address)

        params = self.create_dt_params(columns)
        rowTable = DataTables(params, query, columns)
        res = rowTable.output_result()

        assert len(res['data']) == 3
        assert 'ID' in res['data'][0]
        assert 'Username' in res['data'][0]
        assert 'Address' in res['data'][0]
        assert 'Created at' in res['data'][0]

    def test_fields_search_filters(self):
        query = self.session.query()

        columns = [
            ColumnDT(User.id, search_method='numeric'),
            ColumnDT(User.name, search_method='string_contains'),
            ColumnDT(User.birthday, search_method='date')]

        user = self.session.query(User).filter(User.id == 4).one()

        params = self.create_dt_params(columns)
        params['columns[0][search][value]'] = '=4'
        params['columns[1][search][value]'] = user.name
        params['columns[2][search][value]'] = '>1965-02-02'
        params['columns[2][search][value]'] = '<=99'
        rowTable = DataTables(params, query, columns)
        res = rowTable.output_result()

        assert len(res['data']) == 1

    def test_calculating_age_on_the_fly(self):
        query = self.session.query().filter(User.id > 5)

        columns = [
            ColumnDT(User.id, search_method='numeric'),
            ColumnDT(User.name, search_method='string_contains'),
            ColumnDT(User.birthday, search_method='date'),
            ColumnDT(func.datetime('now') - User.birthday,
                     search_method='numeric')]

        params = self.create_dt_params(columns)
        rowTable = DataTables(params, query, columns)
        res = rowTable.output_result()

        assert len(res['data']) == 10


class FieldsTest2(BaseTest):

    def setUp(self):
        self.user51 = User(name='User 51')
        self.user52 = User(name='User 52')

        self.session.add(self.user51)
        self.session.add(self.user52)
        self.session.commit()

    def tearDown(self):
        self.session.delete(self.user51)
        self.session.delete(self.user52)
        self.session.commit()

    def test_fields_filtering(self):
        """Test if result's are filtered from global search field."""

        columns = [
            ColumnDT(User.id,),
            ColumnDT(User.name)]

        query = self.session.query().select_from(User)

        params = self.create_dt_params(
            columns, search='51')
        rowTable = DataTables(params, query, columns)
        res = rowTable.output_result()

        assert len(res['data']) == 1
        assert res['recordsTotal'] == '52'
        assert res['recordsFiltered'] == '1'
        assert res['data'][0]['1'] == 'User 51'


class FieldsTest3(BaseTest):

    def setUp(self):
        self.user51 = User(name='Run To')
        self.user52 = User(name='Feeeeear Of')

        self.session.add(self.user51)
        self.session.add(self.user52)
        self.session.commit()

    def tearDown(self):
        self.session.delete(self.user51)
        self.session.delete(self.user52)
        self.session.commit()

    def test_fields_global_search_filtering_with_regex(self):
        """Test if result's are filtered from global search field."""
        columns = [
            ColumnDT(User.id,),
            ColumnDT(User.name)]

        query = self.session.query().select_from(User)

        params = self.create_dt_params(columns, search='Fe*ar')
        params['search[regex]'] = 'true'

        rowTable = DataTables(
            params, query, columns, allow_regex_searches=True)
        res = rowTable.output_result()

        if 'error' in res:
            # unfortunately sqlite doesn't support regexp out of the box'
            assert 'no such function: REGEXP' in res['error']
        else:
            assert len(res['data']) == 1
            assert res['recordsTotal'] == '1'
            assert res['recordsFiltered'] == '1'
            assert res['data'][0]['1'] == 'Feeeeear Of'


class FieldsTest3(BaseTest):

    def setUp(self):
        self.user51 = User(name='User 51')
        self.session.add(self.user51)
        self.session.commit()

    def tearDown(self):
        self.session.delete(self.user51)
        self.session.commit()

    def test_column_not_searchable(self):
        """Test if a column is not searchable."""
        columns = [
            ColumnDT(User.id, mData='ID'),
            ColumnDT(User.name, mData='Username', global_search=False)]

        query = self.session.query().select_from(User)

        params = self.create_dt_params(columns, search='User 51')
        rowTable = DataTables(params, query, columns)
        res = rowTable.output_result()

        assert len(res['data']) == 0
        assert res['recordsTotal'] == '51'
        assert res['recordsFiltered'] == '0'
