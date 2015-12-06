"""Dummy unit tests models."""
import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class User(Base):

    """Define a User."""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    address = relationship('Address', uselist=False, backref=backref('user'))

    def __unicode__(self):
        """Give a readable representation of an instance."""
        return '%s' % self.name

    def __repr__(self):
        """Give a unambiguous representation of an instance."""
        return '<%s#%s>' % (self.__class__.__name__, self.id)

    @hybrid_property
    def dummy(self):
        return '%s%s-DUMMY' % (self.name[0:1], str(self.id))

    @dummy.expression
    def dummy(cls):
        return True


class Address(Base):

    """Define an Address."""

    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    description = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __unicode__(self):
        """Give a readable representation of an instance."""
        return '%s' % (self.id)

    def __repr__(self):
        """Give a unambiguous representation of an instance."""
        return '<%s#%s>' % (self.__class__.__name__, self.id)
