"""DataTables unit tests."""
import unittest
import faker
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from datatables import DataTables, ColumnDT
from datetime import datetime, timedelta
from .models import Base, User, Address
import itertools


class BaseTest(unittest.TestCase):

    """Class defining a DataTables test plan."""

    @classmethod
    def setUpClass(cls):
        """Set up fake database session before all tests."""
        cls.engine = create_engine(
            'sqlite://', echo=False)  # echo=True for debug
        Base.metadata.create_all(cls.engine)
        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()
        cls.populate()

    @classmethod
    def tearDownClass(cls):
        """Set up fake database session before all tests."""
        Base.metadata.drop_all(cls.engine)

    @classmethod
    def populate(cls):
        """Create 3 adresses and 50 users."""

        f = faker.Faker(seed=1)
        addresses = [Address(description=d)
                     for d in ['Street', 'Avenue', 'Road']]
        cls.session.add_all(addresses)

        users = []
        for i, addr in zip(range(0, 50), itertools.cycle(addresses)):
            user = User(
                name=f.name(),
                address=addr,
                birthday=datetime(1970, 1, 2) + timedelta(days=10 * i)
            )
            users.append(user)

        cls.session.add_all(users)
        cls.session.commit()

    def basic_dt_params(self, columns):
        """Create DataTables input parameters."""
        params = {
            'draw': '1',
            'start': '0',
            'length': '10',
            'search[value]': '',
            'search[regex]': 'false'
        }

        for i, item in enumerate(columns):
            cols = 'columns[%s]' % i
            params['%s%s' % (cols, '[data]')] = i
            params['%s%s' % (cols, '[name]')] = ''
            params['%s%s' % (cols, '[searchable]')] = 'true'
            params['%s%s' % (cols, '[orderable]')] = 'true'
            params['%s%s' % (cols, '[search][value]')] = ''
            params['%s%s' % (cols, '[search][regex]')] = 'false'

        return params


class SearchMethodTests(BaseTest):

    def get_result(self, column, search_method, search_value):
        columns = [ColumnDT(column, search_method=search_method)]
        query = self.session.query()
        params = self.basic_dt_params(columns)
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
        assert "could not convert string to float: 'abc'" in res['error']

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

    def test_group_by(self):

        columns = [
            ColumnDT(func.count(User.id)),
            ColumnDT(Address.id)]

        query = self.session.query().\
            select_from(User).\
            join(Address).\
            group_by(Address)

        params = self.basic_dt_params(columns)
        rowTable = DataTables(params, query, columns)
        res = rowTable.output_result()

        assert len(res['data']) == 3
