"""DataTables unit tests."""
import unittest
import faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datatables import DataTables, ColumnDT

from .models import Base, User, Address


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
        """Create a fake DataTables columns."""
        cols = []

        for col in columns:
            cols.append(ColumnDT(col))

        return cols

    def create_dt_params(self, search='', start=0, length=10, order=None):
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

        for i, item in enumerate(order or [{'column': 0, 'dir': 'asc'}]):
            for key, value in item.items():
                params['order[%s][%s]' % (i, key)] = str(value)

        return params

    def test_list_users(self):
        """Test if it returns a simple users list."""
        self.populate(5)

        columns = self.create_columns(['id', 'name', 'address.description',
                                       'created_at'])

        req = self.create_dt_params()

        rowTable = DataTables(
            req, User, self.session.query(User).join(Address), columns)

        res = rowTable.output_result()

        assert len(res['data']) == 5
        assert res['recordsTotal'] == '5'
        assert res['recordsFiltered'] == '5'

    def test_list_users_with_hybrid_attribute(self):
        """Test if it returns a users list with a Hybrid column."""
        self.populate(5)

        user6, addr6 = self.create_user('Homer', 'Simpson')

        self.session.add(user6)
        self.session.commit()

        columns = self.create_columns(['id', 'dummy', 'name', 'created_at'])

        req = self.create_dt_params()

        rowTable = DataTables(
            req, User, self.session.query(User), columns)

        res = rowTable.output_result()

        assert len(res['data']) == 6
        assert res['data'][5]['1'] == 'H6-DUMMY'
        assert res['data'][5]['2'] == 'Homer'

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

        req = self.create_dt_params(start=10, length=10)

        rowTable = DataTables(
            req, User, self.session.query(User).join(Address), columns)

        res = rowTable.output_result()

        assert len(res['data']) == 2
        assert res['recordsTotal'] == '12'
        assert res['recordsFiltered'] == '12'
        assert res['data'][0]['1'] == 'The Number of'
        assert res['data'][1]['1'] == 'Hallowed Be'

    def test_set_mdata(self):
        """Test if result's data have mData set."""
        self.populate(5)

        columns = []
        columns.append(ColumnDT('id', mData='ID'))
        columns.append(ColumnDT('name', mData='Username'))
        columns.append(ColumnDT('address.description', mData='Address'))
        columns.append(ColumnDT('created_at', mData='Created at'))

        req = self.create_dt_params()

        rowTable = DataTables(
            req, User, self.session.query(User).join(Address), columns)

        res = rowTable.output_result()

        assert len(res['data']) == 5
        assert 'ID' in res['data'][0]
        assert 'Username' in res['data'][0]
        assert 'Address' in res['data'][0]
        assert 'Created at' in res['data'][0]

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

        req = self.create_dt_params(search='Fear')

        rowTable = DataTables(
            req, User, self.session.query(User).join(Address), columns)

        res = rowTable.output_result()

        assert len(res['data']) == 1
        assert res['recordsTotal'] == '7'
        assert res['recordsFiltered'] == '1'
        assert res['data'][0]['1'] == 'Fear Of'
        assert res['data'][0]['2'] == 'The Dark'

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

        req = self.create_dt_params(search='Fear')

        rowTable = DataTables(
            req, User, self.session.query(User).join(Address), columns)

        res = rowTable.output_result()

        assert len(res['data']) == 0
        assert res['recordsTotal'] == '7'
        assert res['recordsFiltered'] == '0'

    def test_null_field_filtering(self):
        """Test if a None field is not filtered."""
        self.populate(5)

        user6, addr6 = self.create_user('Empty', None)

        self.session.add(user6)
        self.session.commit()

        columns = self.create_columns(['id', 'name', 'address.description',
                                       'created_at'])

        req = self.create_dt_params()

        rowTable = DataTables(
            req, User, self.session.query(User).join(Address), columns)

        res = rowTable.output_result()

        assert len(res['data']) == 6
        assert res['recordsTotal'] == '6'
        assert res['recordsFiltered'] == '6'

    def test_column_ordering(self):
        """Test if a column is orderable."""
        self.populate(5)

        user6, addr6 = self.create_user('000_aaa', 'Whatever')
        user7, addr7 = self.create_user('zzz_aaa', 'Whatif')

        self.session.add(user6)
        self.session.add(user7)
        self.session.commit()

        columns = self.create_columns(['id', 'name', 'address.description',
                                       'created_at'])

        # DESC
        req = self.create_dt_params(order=[{"column": 1, "dir": "desc"}])

        rowTable = DataTables(
            req, User, self.session.query(User).join(Address), columns)

        res = rowTable.output_result()

        assert res['data'][0]['1'] == 'zzz_aaa'

        # ASC
        req = self.create_dt_params(order=[{"column": 1, "dir": "asc"}])

        rowTable = DataTables(
            req, User, self.session.query(User).join(Address), columns)

        res = rowTable.output_result()

        assert res['data'][0]['1'] == '000_aaa'

        # DESC first column
        req = self.create_dt_params(order=[{"column": 0, "dir": "desc"}])

        rowTable = DataTables(
            req, User, self.session.query(User).join(Address), columns)

        res = rowTable.output_result()

        assert res['data'][0]['1'] == 'zzz_aaa'

    def test_column_ordering_relation(self):
        """Test if a foreign key column is orderable."""
        self.populate(5)

        user6, addr6 = self.create_user('000_Whatever', '000_aaa')
        user7, addr7 = self.create_user('zzz_Whatif', 'zzz_aaa')

        self.session.add(user6)
        self.session.add(user7)
        self.session.commit()

        columns = self.create_columns(['id', 'name', 'address.description',
                                       'created_at'])

        # DESC
        req = self.create_dt_params(order=[{"column": 2, "dir": "desc"}])

        rowTable = DataTables(
            req, User, self.session.query(User).join(Address), columns)

        res = rowTable.output_result()

        assert res['data'][0]['2'] == 'zzz_aaa'

        # ASC
        req = self.create_dt_params(order=[{"column": 2, "dir": "asc"}])

        rowTable = DataTables(
            req, User, self.session.query(User).join(Address), columns)

        res = rowTable.output_result()

        assert res['data'][0]['2'] == '000_aaa'
