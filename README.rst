=================================================================
`sqlalchemy-datatables <http://sqlalchemy-datatables.rtfd.org/>`_
=================================================================

sqlalchemy-datatables is a library providing an `SQLAlchemy <http://www.sqlalchemy.org/>`_ integration of jQuery `DataTables <http://datatables.net/>`_. It helps you manage server side requests in your application.

It is framework agnostic, tested with `Pyramid <http://www.pylonsproject.org/>`_ and `Flask <http://flask.pocoo.org/>`_ mainly.

It only depends on SQLAlchemy, and is compatible with version **1.10.x** of DataTables.

|Build Status| |PyPi Version| |Python Versions| |Coverage| |PyPi Downloads|

.. |Build Status| image:: https://img.shields.io/travis/Pegase745/sqlalchemy-datatables.svg?style=flat-square
    :target: https://travis-ci.org/Pegase745/sqlalchemy-datatables

.. |PyPi Version| image:: https://img.shields.io/pypi/v/sqlalchemy-datatables.svg?style=flat-square
    :target: https://pypi.python.org/pypi/sqlalchemy-datatables/

.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/sqlalchemy-datatables.svg?style=flat-square
    :target: https://pypi.python.org/pypi/sqlalchemy-datatables/

.. |Coverage| image:: https://img.shields.io/codecov/c/github/Pegase745/sqlalchemy-datatables.svg?style=flat-square
    :target: https://codecov.io/gh/Pegase745/sqlalchemy-datatables

.. |PyPi Downloads| image:: https://img.shields.io/pypi/dm/sqlalchemy-datatables.svg?style=flat-square
    :target: https://pypi.python.org/pypi/sqlalchemy-datatables/

Installation
------------

To install the stable version:

.. code-block:: bash

    pip install sqlalchemy-datatables


Usage
-----

**views.py**

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


You can find detailed a working example for Pyramid in the repository, including per column search, and one with the `yadcf <https://github.com/vedmack/yadcf/>`_ plugin. Currently the Flask example is not working

**Pyramid example:**

.. code-block:: bash

    # go to directory
    cd sqlalchemy-datatables/examples/pyramid_tut

    # install example app
    pip install -e .

    # initialize the database
    initialize_pyramid_tut_db development.ini

    # start server
    pserve development.ini

    # browse to localhost:6543

Documentation
-------------

The latest documentation is available online on `Read the Docs <http://sqlalchemy-datatables.readthedocs.org/en/latest/>`_.

Changelog
---------

All notable changes to this project will be documented in `this section <CHANGELOG.rst>`_.

This project adheres to `Semantic Versioning <http://semver.org/>`_ and `Keep A Changelog <http://keepachangelog.com/>`_.

License
-------

The project is licensed under the MIT license.
