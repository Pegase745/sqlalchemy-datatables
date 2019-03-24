======================
sqlalchemy-datatables
======================

|Build Status| |PyPi Version| |Scrutinizer| |Coverage|

.. |Build Status| image:: https://travis-ci.org/Pegase745/sqlalchemy-datatables.svg?branch=master
    :target: https://travis-ci.org/Pegase745/sqlalchemy-datatables

.. |PyPi Version| image:: https://badge.fury.io/py/sqlalchemy-datatables.svg
    :target: https://pypi.python.org/pypi/sqlalchemy-datatables/

.. |Scrutinizer| image:: https://scrutinizer-ci.com/g/Pegase745/sqlalchemy-datatables/badges/quality-score.png
    :target: https://scrutinizer-ci.com/g/Pegase745/sqlalchemy-datatables/

.. |Coverage| image:: https://codecov.io/gh/Pegase745/sqlalchemy-datatables/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Pegase745/sqlalchemy-datatables

sqlalchemy-datatables is a framework agnostic library providing an `SQLAlchemy <http://www.sqlalchemy.org/>`_ integration of jQuery `DataTables <http://datatables.net/>`_ >= 1.10, and helping you manage server side requests in your application.

Installation
------------

**To install via pip:**

*Python 3*

.. code-block:: bash

    $ pip3 install sqlalchemy-datatables

**To install from source:**

.. code-block:: bash

    $ git clone git@github.com:Pegase745/sqlalchemy-datatables.git
    $ cd sqlalchemy-datatables
    $ pip3 install .

**To contribute:**

.. code-block:: bash

    In a virtualenv
    $ git clone git@github.com:Pegase745/sqlalchemy-datatables.git
    $ cd sqlalchemy-datatables
    $ make all

Usage
-----

.. code-block:: python

    @view_config(route_name='data', renderer='json')
    def data(request):
        """Return server side data."""
        # defining columns
        #  - explicitly cast date to string, so string searching the date
        #    will search a date formatted equal to how it is presented
        #    in the table
        columns = [
            ColumnDT(User.id),
            ColumnDT(User.name),
            ColumnDT(Address.description),
            ColumnDT(func.strftime('%d-%m-%Y', User.birthday)),
            ColumnDT(User.age)
        ]

        # defining the initial query depending on your purpose
        #  - don't include any columns
        #  - if you need a join, also include a 'select_from'
        query = DBSession.query().\
            select_from(User).\
            join(Address).\
            filter(Address.id > 4)

        # instantiating a DataTable for the query and table needed
        rowTable = DataTables(request.GET, query, columns)

        # returns what is needed by DataTable
        return rowTable.output_result()

Examples
--------

You can find working examples `in the repository <examples>`_, including an integration with the `yadcf <https://github.com/vedmack/yadcf/>`_ plugin:

- `Pyramid example <examples/pyramid_tut/README.rst>`_
- `Flask example <examples/flask_tut/README.rst>`_

Changelog
---------

All notable changes to this project will be documented in `this section <https://github.com/Pegase745/sqlalchemy-datatables/releases>`_.

This project adheres to `Semantic Versioning <http://semver.org/>`_ and `Keep A Changelog <http://keepachangelog.com/>`_.

License
-------

The project is licensed under the MIT license.
