"""Flask tutorial models.

Basic example: a User has one or many Addresses.
"""
import datetime
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('../app.cfg')
db = SQLAlchemy(app)


class User(db.Model):

    """Define a User."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    address = db.relationship(
        'Address', uselist=False, backref=db.backref('user'))

    def __unicode__(self):
        """Give a readable representation of an instance."""
        return '%s' % self.name

    def __repr__(self):
        """Give a unambiguous representation of an instance."""
        return '<%s#%s>' % (self.__class__.__name__, self.id)


class Address(db.Model):

    """Define an Address."""

    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Unicode, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __unicode__(self):
        """Give a readable representation of an instance."""
        return '%s' % (self.id)

    def __repr__(self):
        """Give a unambiguous representation of an instance."""
        return '<%s#%s>' % (self.__class__.__name__, self.id)
