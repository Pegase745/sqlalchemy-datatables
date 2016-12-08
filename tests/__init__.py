"""DataTables unit tests."""
import faker
import unittest
import itertools

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from .models import Base, User, Address


class BaseTest(unittest.TestCase):

    """Class defining base test methods."""

    @classmethod
    def setUpClass(cls):
        """Set up fake database session before all tests."""
        cls.engine = create_engine(
            'sqlite:///db.sqlite', echo=False)  # echo=True for debug
        Base.metadata.create_all(cls.engine)
        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()
        cls.populate()

    @classmethod
    def tearDownClass(cls):
        """Tear down database session after all tests."""
        Base.metadata.drop_all(cls.engine)

    @classmethod
    def populate(cls):
        """Create 3 adresses and 50 users."""
        users = []
        f = faker.Faker(seed=1)
        addresses = [Address(description=d)
                     for d in ['Street', 'Avenue', 'Road']]
        cls.session.add_all(addresses)

        for i, addr in zip(range(0, 50), itertools.cycle(addresses)):
            user = User(
                name=f.name(),
                address=addr,
                birthday=datetime(1970, 1, 2) + timedelta(days=10 * i)
            )
            users.append(user)

        cls.session.add_all(users)
        cls.session.commit()

    def create_dt_params(
            self, columns, search='', start=0, length=10, order=None):
        """Create DataTables input parameters."""
        params = {
            'draw': '1',
            'start': str(start),
            'length': str(length),
            'search[value]': str(search),
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

        for i, item in enumerate(order or [{'column': 0, 'dir': 'asc'}]):
            for key, value in item.items():
                params['order[%s][%s]' % (i, key)] = str(value)

        return params

    def create_user(self, name, address, birthday=datetime.now()):
        """Create a custom fake user."""
        addr = Address(description=address)

        user = User(name=name, address=addr, birthday=birthday)

        return user, addr
