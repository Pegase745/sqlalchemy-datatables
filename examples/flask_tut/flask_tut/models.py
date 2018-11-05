import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
        return '{}'.format(self.name)

    def __repr__(self):
        """Give a unambiguous representation of an instance."""
        return '<{}#{}>'.format(self.__class__.__name__, self.id)


class Address(db.Model):
    """Define an Address."""

    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Unicode, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __unicode__(self):
        """Give a readable representation of an instance."""
        return '{}'.format(self.id)

    def __repr__(self):
        """Give a unambiguous representation of an instance."""
        return '<{}#{}>'.format(self.__class__.__name__, self.id)
