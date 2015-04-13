from __future__ import absolute_import, unicode_literals

import datetime

from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    address = relationship("Address", uselist=False, backref="user")

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "%s" % self.name

    def __repr__(self):
        return '<%s#%s>' % (self.__class__.__name__, self.id)


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    description = Column(Text, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, description):
        self.description = description

    def __str__(self):
        return "%s" % (self.id)

    def __repr__(self):
        return '<%s#%s>' % (self.__class__.__name__, self.id)
