from time import sleep

import click
from datatables import ColumnDT, DataTables
from flask import Flask, jsonify, render_template, request
from flask_tut.models import Address, User, db

app = Flask(__name__)
app.config.from_pyfile('../app.cfg')
db.init_app(app)


@app.cli.command()
def initdb():
    """Initialize the database."""
    click.echo('Init the db...')
    db.create_all()

    for i in range(30):
        click.echo("Creating user/address combo #{}...".format(i))
        address = Address(description='Address#2' + str(i).rjust(2, "0"))
        db.session.add(address)
        user = User(name='User#1' + str(i).rjust(2, "0"))
        user.address = address
        db.session.add(user)
        sleep(1)
    db.session.commit()


@app.route("/")
def home():
    """Try to connect to database, and list available examples."""
    return render_template('home.html', project='flask_tut')


@app.route("/dt_110x")
def dt_110x():
    """List users with DataTables <= 1.10.x."""
    return render_template('dt_110x.html', project='dt_110x')


@app.route('/data')
def data():
    """Return server side data."""
    # defining columns
    columns = [
        ColumnDT(User.id),
        ColumnDT(User.name),
        ColumnDT(Address.description),
        ColumnDT(User.created_at)
    ]

    # defining the initial query depending on your purpose
    query = db.session.query().select_from(User).join(Address).filter(
        Address.id > 14)

    # GET parameters
    params = request.args.to_dict()

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(params, query, columns)

    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())
