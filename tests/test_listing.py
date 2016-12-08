"""Column DataTable unit tests."""
from datatables import DataTables, ColumnDT

from . import BaseTest
from .models import User, Address


class ListingTest(BaseTest):

    """Class defining a test plan for listing elements."""

    def test_list(self):
        """Test if it returns a list of users."""
        columns = [ColumnDT(User.id)]

        query = self.session.query().select_from(User)

        params = self.create_dt_params(columns)
        rowTable = DataTables(params, query, columns)
        res = rowTable.output_result()

        assert len(res['data']) == 10
        assert len(res['data'][0]) == 1
        assert res['recordsTotal'] == '50'
        assert res['recordsFiltered'] == '50'

    def test_list_bad_length(self):
        """Test if it returns an error for querying with a bad length."""
        columns = [ColumnDT(User.id)]

        query = self.session.query()

        params = self.create_dt_params(columns, length=-10)
        rowTable = DataTables(params, query, columns)
        res = rowTable.output_result()

        assert 'Length should be' in res['error']

    def test_list_detail(self):
        """Test if it returns a list of detailed users."""
        columns = [
            ColumnDT(User.id),
            ColumnDT(User.name),
            ColumnDT(Address.description),
            ColumnDT(User.created_at)]

        query = self.session.query()

        params = self.create_dt_params(columns)
        rowTable = DataTables(params, query, columns)
        res = rowTable.output_result()

        assert len(res['data'][0]) == 4

    def test_list_fixed_length(self):
        """Test if it returns a fixed list of users."""
        columns = [ColumnDT(User.id)]

        query = self.session.query()

        params = self.create_dt_params(columns, length=7)
        rowTable = DataTables(params, query, columns)
        res = rowTable.output_result()

        assert len(res['data']) == 7

    def test_list_inner_join(self):
        """Test if it returns a list of users with address."""
        columns = [ColumnDT(User.id)]

        query = self.session.query().select_from(User).join(Address)

        params = self.create_dt_params(columns)
        rowTable = DataTables(params, query, columns)
        res = rowTable.output_result()

        assert len(res['data']) == 3
        assert res['recordsTotal'] == '3'
        assert res['recordsFiltered'] == '3'

    def test_list_total_length(self):
        """Test if it returns the total list of users."""
        columns = [ColumnDT(User.id)]

        query = self.session.query()

        params = self.create_dt_params(columns, length=-1)
        rowTable = DataTables(params, query, columns)
        res = rowTable.output_result()

        assert len(res['data']) == 50


class ListingTest2(BaseTest):

    """Class defining a test plan for listing elements."""

    def setUp(self):
        """Set up fake population before tests."""
        self.user51 = User(name='User 51')
        self.session.add(self.user51)
        self.session.commit()

    def tearDown(self):
        """Tear down fake population after tests."""
        self.session.delete(self.user51)
        self.session.commit()

    def test_list_hybrid_attributes(self):
        """Test if it returns a list of users with a hybrid property."""
        columns = [
            ColumnDT(User.id),
            ColumnDT(User.dummy),
            ColumnDT(User.name),
            ColumnDT(User.created_at)]

        self.session.query(*[User.id, User.dummy]).all()

        query = self.session.query()

        params = self.create_dt_params(columns, start=50, length=10)
        rowTable = DataTables(params, query, columns)
        res = rowTable.output_result()

        assert len(res['data']) == 1
        assert res['data'][0]['1'] == 'Us'
        assert res['data'][0]['2'] == 'User 51'


class ListingTest3(BaseTest):

    """Class defining a test plan for listing elements."""

    def setUp(self):
        """Set up fake population before tests."""
        self.user51 = User(name='User 51')
        self.user52 = User(name='User 52')
        self.session.add(self.user51)
        self.session.add(self.user52)
        self.session.commit()

    def tearDown(self):
        """Tear down fake population after tests."""
        self.session.delete(self.user51)
        self.session.delete(self.user52)
        self.session.commit()

    def test_list_specific_page(self):
        """Test if it returns the list of users that are on page 6."""
        columns = [ColumnDT(User.id)]

        query = self.session.query().select_from(User)

        params = self.create_dt_params(columns, start=50, length=10)
        rowTable = DataTables(params, query, columns)
        res = rowTable.output_result()

        assert len(res['data']) == 2
        assert res['recordsTotal'] == '52'
        assert res['recordsFiltered'] == '52'
        assert res['data'][0]['0'] == 51
        assert res['data'][1]['0'] == 52
