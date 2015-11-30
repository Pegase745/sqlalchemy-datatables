"""Pyramid tutorial models.

Basic example: a User has one or many Addresses.
"""
import datetime

from sqlalchemy import Column, Integer, Unicode, DateTime, ForeignKey
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

    """Define a User."""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    address = relationship('Address', uselist=False, backref=backref('user'))

    def __unicode__(self):
        """Give a readable representation of an instance."""
        return '%s' % self.name

    def __repr__(self):
        """Give a unambiguous representation of an instance."""
        return '<%s#%s>' % (self.__class__.__name__, self.id)


class Address(Base):

    """Define an Address."""

    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    description = Column(Unicode, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __unicode__(self):
        """Give a readable representation of an instance."""
        return '%s' % (self.id)

    def __repr__(self):
        """Give a unambiguous representation of an instance."""
        return '<%s#%s>' % (self.__class__.__name__, self.id)
