"""Flask tutorial views."""
from string import upper
from flask import Flask, render_template, request, jsonify

from datatables import ColumnDT, DataTables

from flask_tut.models import (
    db,
    User,
    Address,
)

app = Flask(__name__)
app.config['sqlalchemy.url'] = 'sqlite:////tmp/flask_tut.sqlite'
db.init_app(app)


@app.route('/', methods=['GET'])
def home():
    """Try to connect to database, and list available examples."""
    return render_template('home.html', project='flask_tut')


@app.route('/dt_19x', methods=['GET'])
def dt_19x():
    """List users with DataTables <= 1.9.x."""
    return render_template('dt_19x.html', project='dt_19x')


@app.route('/dt_110x', methods=['GET'])
def dt_110x():
    """List users with DataTables <= 1.10.x."""
    return render_template('dt_110x.html', project='dt_110x')


@app.route('/data')
def data():
    """Return server side data."""
    # defining columns
    columns = []
    columns.append(ColumnDT('id'))
    columns.append(ColumnDT('name', filter=upper))
    columns.append(ColumnDT('address.description'))
    columns.append(ColumnDT('created_at'))

    # defining the initial query depending on your purpose
    query = db.session.query(User).join(Address).filter(Address.id > 14)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.args, User, query, columns)

    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())


if __name__ == '__main__':
    app.run('0.0.0.0', port=5678, debug=True)
