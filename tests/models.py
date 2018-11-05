import datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref, relationship

Base = declarative_base()


class User(Base):
    """Define a User."""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    birthday = Column(Date)
    address = relationship('Address', uselist=False, backref=backref('user'))

    def __unicode__(self):
        """Give a readable representation of an instance."""
        return '%s' % self.name

    def __repr__(self):
        """Give a unambiguous representation of an instance."""
        return '<%s#%s>' % (self.__class__.__name__, self.id)

    @hybrid_property
    def dummy(self):
        """Create a dummy hybrid property."""
        return self.name[0:3]

    @dummy.expression
    def dummy(cls):
        """Create a dummy expression."""
        return func.substr(cls.name, 0, 3)


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
