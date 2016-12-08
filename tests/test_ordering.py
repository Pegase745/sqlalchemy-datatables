"""Column DataTable unit tests."""
from datatables import DataTables, ColumnDT

from . import BaseTest
from .models import User, Address


class OrderingTest(BaseTest):

    def setUp(self):
        self.user51 = User(name='000_User')
        self.user52 = User(name='zzz_User')
        self.addr4 = Address(description='000_Address')
        self.addr5 = Address(description='zzz_Address')
        self.user53 = User(name='UserFirstAddress', address=self.addr4)
        self.user54 = User(name='UserLastAddress', address=self.addr5)
        self.session.add(self.user51)
        self.session.add(self.user52)
        self.session.add(self.user53)
        self.session.add(self.user54)
        self.session.commit()

    def tearDown(self):

        self.session.delete(self.user51)
        self.session.delete(self.user52)
        self.session.delete(self.user53)
        self.session.delete(self.user54)
        self.session.delete(self.addr4)
        self.session.delete(self.addr5)
        self.session.commit()

    """Class defining a test plan for ordering elements."""

    def test_ordering(self):
        """Test if it returns a list with the correct order."""

        columns = [
            ColumnDT(User.id,),
            ColumnDT(User.name)]

        query = self.session.query().select_from(User)

        # Descending
        params = self.create_dt_params(columns,
                                       order=[{"column": 1, "dir": "desc"}])
        rowTable = DataTables(params, query, columns)
        res = rowTable.output_result()

        assert res['data'][0]['1'] == 'zzz_User'

        # Ascending
        params = self.create_dt_params(columns,
                                       order=[{"column": 1, "dir": "asc"}])

        rowTable = DataTables(params, query, columns)
        res = rowTable.output_result()

        assert res['data'][0]['1'] == '000_User'

    def test_ordering_nulls(self):
        """Test if it returns a list with the correct nulls order."""

        columns = [
            ColumnDT(User.id,),
            ColumnDT(User.name),
            ColumnDT(Address.description, nulls_order='nullsfirst'),
            ColumnDT(User.created_at)]

        query = self.session.query().select_from(User).join(Address)

        # NULLS FIRST
        params = self.create_dt_params(columns,
                                       order=[{"column": 2, "dir": "desc"}])
        rowTable = DataTables(params, query, columns)
        res = rowTable.output_result()

        if 'error' in res:
            # sqlite3 doesn't support nulls ordering
            assert 'sqlite3.OperationalError) near "NULLS"' in res['error']

        columns = [
            ColumnDT(User.id,),
            ColumnDT(User.name),
            ColumnDT(Address.description, nulls_order='nullslast'),
            ColumnDT(User.created_at)]

        # NULLS LAST
        params = self.create_dt_params(columns,
                                       order=[{"column": 2, "dir": "asc"}])

        rowTable = DataTables(params, query, columns)
        res = rowTable.output_result()

        if 'error' in res:
            # sqlite3 doesn't support nulls ordering
            assert 'sqlite3.OperationalError) near "NULLS"' in res['error']

    def test_ordering_relation(self):
        """Test if it returns a list when ordering a foreign key."""
        columns = [
            ColumnDT(User.id,),
            ColumnDT(User.name),
            ColumnDT(Address.description),
            ColumnDT(User.created_at)]

        query = self.session.query().select_from(User).join(Address)

        # Descending
        params = self.create_dt_params(columns,
                                       order=[{"column": 2, "dir": "desc"}])
        rowTable = DataTables(params, query, columns)
        res = rowTable.output_result()

        assert res['data'][0]['1'] == 'UserLastAddress'
        assert res['data'][0]['2'] == 'zzz_Address'

        columns = [
            ColumnDT(User.id,),
            ColumnDT(User.name),
            ColumnDT(Address.description),
            ColumnDT(User.created_at)]

        # Ascending
        params = self.create_dt_params(columns,
                                       order=[{"column": 2, "dir": "asc"}])

        rowTable = DataTables(params, query, columns)
        res = rowTable.output_result()

        assert res['data'][0]['1'] == 'UserFirstAddress'
        assert res['data'][0]['2'] == '000_Address'
