from __future__ import print_function

import itertools
from datetime import datetime, timedelta

import faker
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Address, Base, User


def populate(session):
    """Create 3 adresses and 50 users."""
    users = []
    f = faker.Faker(seed=1)
    addresses = [Address(description=d) for d in ['Street', 'Avenue', 'Road']]
    session.add_all(addresses)

    for i, addr in zip(range(0, 50), itertools.cycle(addresses)):
        user = User(
            name=f.name(),
            address=addr,
            birthday=datetime(1970, 1, 2) + timedelta(days=10 * i))
        users.append(user)

    session.add_all(users)
    session.commit()


@pytest.fixture(scope="session")
def engine():
    print("TestCase: Using sqlite database")
    return create_engine('sqlite:///', echo=False)


@pytest.fixture(scope="session")
def session(engine):
    sessionmaker_ = sessionmaker(bind=engine)
    session = sessionmaker_()
    Base.metadata.create_all(engine)
    populate(session)

    yield session

    session.close()
