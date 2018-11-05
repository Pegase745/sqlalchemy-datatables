"""Flask tutorial views."""

from datatables import ColumnDT, DataTables
from flask import Flask, jsonify, render_template, request
from flask_tut.models import Address, User, db

app = Flask(__name__)

app.config.from_pyfile("../app.cfg")

db.init_app(app)

@app.route("/")
def home():
    """Try to connect to database, and list available examples."""

    return render_template("home.html", project="flask_tut")

@app.route("/dt_110x")
def dt_110x():
    """List users with DataTables <= 1.10.x."""

    return render_template("dt_110x.html", project="dt_110x")

@app.route("/data")
def data():
    """Return server side data."""

    columns = [ColumnDT(User.id), ColumnDT(User.name), ColumnDT(Address.description), ColumnDT(User.created_at)]

    query = db.session.query().select_from(User).join(Address).filter(Address.id > 14)

    params = request.args.to_dict()

    rowTable = DataTables(params, query, columns)

    return jsonify(rowTable.output_result())

if __name__ == "__main__":
    app.run("0.0.0.0", port=5678, debug=True)
