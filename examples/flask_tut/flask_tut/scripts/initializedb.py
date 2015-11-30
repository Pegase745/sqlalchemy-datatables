"""Initialize DB with fixtures."""
from time import sleep
from flask import Flask
from flask_tut.models import (
    db,
    User,
    Address,
)

app = Flask(__name__)

with app.app_context():
    db.create_all()

i = 0
while i < 30:
    address = Address(description='Address#2' + str(i).rjust(2, "0"))
    db.session.add(address)
    user = User(name='User#1' + str(i).rjust(2, "0"))
    user.address = address
    db.session.add(user)
    sleep(1)
    i += 1
db.session.commit()
