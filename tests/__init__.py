"""Unit tests execution plan."""
import unittest
import faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datatables import DataTables, ColumnDT

from .models import Base, User, Address


class ColumnTest(unittest.TestCase):

    """Class defining a DataTables Column test plan."""

    def test_with_default_params_ok(self):
        """Return column with given default params."""
        col = ColumnDT('id')

        assert col.column_name == 'id'
        assert col.filter(col.column_name) == 'id'

    def test_with_filter_ok(self):
        """Return column with a specific filter."""
        col = ColumnDT('id', filter=lambda x: 'HANDLE %s' % x)

        assert col.filter(col.column_name) == 'HANDLE id'


class DataTablesTest(unittest.TestCase):

    """Class defining a DataTables test plan."""

    def setUp(self):
        """Set up fake database session before all tests."""
        engine = create_engine('sqlite://', echo=False)  # echo=True for debug
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def populate(self, nbUsers):
        """Create nbUsers in fake database."""
        users = []
        f = faker.Faker()

        for i in range(nbUsers):
            user, addr = self.create_user(f.name(), f.address())
            users.append(user)

        self.session.add_all(users)
        self.session.commit()

    def create_user(self, name, address):
        """Create a fake user."""
        addr = Address(description=address)

        user = User(name=name, address=addr)

        return user, addr

    def create_columns(self, columns):
        cols = []

        for col in columns:
            cols.append(ColumnDT(col))

        return cols

    def create_dt_params(self, search='', start=0, length=10):
        """Create DataTables input parameters."""
        params = {
            'draw': '1',
            'start': str(start),
            'length': str(length),
            'search[value]': str(search),
            'search[regex]': 'false'
        }

        for i, item in enumerate(('id', 'name', 'address', 'created_at')):
            cols = 'columns[%s]' % i
            params['%s%s' % (cols, '[data]')] = i
            params['%s%s' % (cols, '[name]')] = ''
            params['%s%s' % (cols, '[searchable]')] = 'true'
            params['%s%s' % (cols, '[orderable]')] = 'true'
            params['%s%s' % (cols, '[search][value]')] = ''
            params['%s%s' % (cols, '[search][regex]')] = 'false'

        return params

    def create_dt_legacy_params(self, search='', start=0, length=10):
        """Create DataTables input parameters."""
        params = {
            'sEcho': '1',
            'iDisplayStart': str(start),
            'iDisplayLength': str(length),
            'bRegex': 'false',
            'iSortingCols': '1',
            'sSearch': str(search)
        }

        for i, item in enumerate(('id', 'name', 'address', 'created_at')):
            params['mDataProp_%s' % i] = i
            params['sSearch_%s' % i] = ''
            params['bRegex_%s' % i] = 'false'
            params['bSearchable_%s' % i] = 'true'
            params['bSortable_%s' % i] = 'true'

        params['iColumns'] = '4'
        params['sColumns'] = ''
        params['iSortCol_0'] = '0'
        params['sSortDir_0'] = 'asc'

        return params

    def test_list_users(self):
        """Test if it returns a simple users list."""
        self.populate(5)

        columns = []
        columns.append(ColumnDT('id'))
        columns.append(ColumnDT('name'))
        columns.append(ColumnDT('address.description'))
        columns.append(ColumnDT('created_at'))

        # LATEST
        req = self.create_dt_params()

        rowTable = DataTables(
            req, User, self.session.query(User).join(Address), columns)

        res = rowTable.output_result()

        assert len(res['data']) == 5
        assert res['recordsTotal'] == '5'
        assert res['recordsFiltered'] == '5'

        # LEGACY
        req = self.create_dt_legacy_params()

        rowTable = DataTables(
            req, User, self.session.query(User).join(Address), columns)

        res = rowTable.output_result()

        assert len(res['aaData']) == 5
        assert res['iTotalRecords'] == '5'
        assert res['iTotalDisplayRecords'] == '5'

    def test_list_page_x(self):
        """Test if it lists users that are not on page 1."""
        self.populate(10)

        user11, addr11 = self.create_user('The Number of', 'The Beast')
        user12, addr12 = self.create_user('Hallowed Be', 'Thy Name')

        self.session.add(user11)
        self.session.add(user12)
        self.session.commit()

        columns = self.create_columns(['id', 'name', 'address.description',
                                       'created_at'])

        # LATEST
        req = self.create_dt_params(start=10, length=10)

        rowTable = DataTables(
            req, User, self.session.query(User).join(Address), columns)

        res = rowTable.output_result()

        assert len(res['data']) == 2
        assert res['recordsTotal'] == '12'
        assert res['recordsFiltered'] == '12'
        assert res['data'][0]['1'] == 'The Number of'
        assert res['data'][1]['1'] == 'Hallowed Be'

        # LEGACY
        req = self.create_dt_legacy_params(start=10, length=10)

        rowTable = DataTables(
            req, User, self.session.query(User).join(Address), columns)

        res = rowTable.output_result()

        assert len(res['aaData']) == 2
        assert res['iTotalRecords'] == '12'
        assert res['iTotalDisplayRecords'] == '12'
        assert res['aaData'][0]['1'] == 'The Number of'
        assert res['aaData'][1]['1'] == 'Hallowed Be'

    def test_set_mdata(self):
        """Test if result's data have mData set."""
        self.populate(5)

        columns = []
        columns.append(ColumnDT('id', mData='ID'))
        columns.append(ColumnDT('name', mData='Username'))
        columns.append(ColumnDT('address.description', mData='Address'))
        columns.append(ColumnDT('created_at', mData='Created at'))

        # LATEST
        req = self.create_dt_params()

        rowTable = DataTables(
            req, User, self.session.query(User).join(Address), columns)

        res = rowTable.output_result()

        assert len(res['data']) == 5
        assert 'ID' in res['data'][0]
        assert 'Username' in res['data'][0]
        assert 'Address' in res['data'][0]
        assert 'Created at' in res['data'][0]

        # LEGACY
        req = self.create_dt_legacy_params()

        rowTable = DataTables(
            req, User, self.session.query(User).join(Address), columns)

        res = rowTable.output_result()

        assert len(res['aaData']) == 5
        assert 'ID' in res['aaData'][0]
        assert 'Username' in res['aaData'][0]
        assert 'Address' in res['aaData'][0]
        assert 'Created at' in res['aaData'][0]

    def test_global_search_filtering(self):
        """Test if result's are filtered from global search field."""
        self.populate(5)

        user6, addr6 = self.create_user('Run To', 'The Hills')
        user7, addr7 = self.create_user('Fear Of', 'The Dark')

        self.session.add(user6)
        self.session.add(user7)
        self.session.commit()

        columns = self.create_columns(['id', 'name', 'address.description',
                                       'created_at'])

        # LATEST
        req = self.create_dt_params(search='Fear')

        rowTable = DataTables(
            req, User, self.session.query(User).join(Address), columns)

        res = rowTable.output_result()

        assert len(res['data']) == 1
        assert res['recordsTotal'] == '7'
        assert res['recordsFiltered'] == '1'
        assert res['data'][0]['1'] == 'Fear Of'
        assert res['data'][0]['2'] == 'The Dark'

        # LEGACY
        req = self.create_dt_legacy_params(search='Fear')

        rowTable = DataTables(
            req, User, self.session.query(User).join(Address), columns)

        res = rowTable.output_result()

        assert len(res['aaData']) == 1
        assert res['iTotalRecords'] == '7'
        assert res['iTotalDisplayRecords'] == '1'
        assert res['aaData'][0]['1'] == 'Fear Of'
        assert res['aaData'][0]['2'] == 'The Dark'

    def test_column_not_searchable(self):
        """Test if a column is not searchable."""
        self.populate(5)

        user6, addr6 = self.create_user('Run To', 'The Hills')
        user7, addr7 = self.create_user('Fear Of', 'The Dark')

        self.session.add(user6)
        self.session.add(user7)
        self.session.commit()

        columns = []
        columns.append(ColumnDT('id', mData='ID'))
        columns.append(ColumnDT('name', mData='Username', searchable=False))
        columns.append(ColumnDT('address.description', mData='Address'))
        columns.append(ColumnDT('created_at', mData='Created at'))

        # LATEST
        req = self.create_dt_params(search='Fear')

        rowTable = DataTables(
            req, User, self.session.query(User).join(Address), columns)

        res = rowTable.output_result()

        assert len(res['data']) == 0
        assert res['recordsTotal'] == '7'
        assert res['recordsFiltered'] == '0'

        # LEGACY
        req = self.create_dt_legacy_params(search='Fear')

        rowTable = DataTables(
            req, User, self.session.query(User).join(Address), columns)

        res = rowTable.output_result()

        assert len(res['aaData']) == 0
        assert res['iTotalRecords'] == '7'
        assert res['iTotalDisplayRecords'] == '0'
