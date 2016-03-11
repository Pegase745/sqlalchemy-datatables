=================================================================
`sqlalchemy-datatables <http://sqlalchemy-datatables.rtfd.org/>`_
=================================================================

sqlalchemy-datatables is a library providing an `SQLAlchemy <http://www.sqlalchemy.org/>`_ integration of jQuery `DataTables <http://datatables.net/>`_. It helps you manage server side requests in your application.

It is framework agnostic, tested with `Pyramid <http://www.pylonsproject.org/>`_ and `Flask <http://flask.pocoo.org/>`_ mainly.

It only depends on SQLAlchemy, and is compatible with versions **1.9.x** and **1.10.x** of DataTables.

|Build Status| |PyPi Version| |PyPi Downloads| |Code Quality| |Coveralls|

.. |Build Status| image:: https://img.shields.io/travis/Pegase745/sqlalchemy-datatables.svg?style=flat-square
    :target: https://travis-ci.org/Pegase745/sqlalchemy-datatables

.. |PyPi Version| image:: https://img.shields.io/pypi/v/sqlalchemy-datatables.svg?style=flat-square
    :target: https://pypi.python.org/pypi/sqlalchemy-datatables/

.. |PyPi Downloads| image:: https://img.shields.io/pypi/dm/sqlalchemy-datatables.svg?style=flat-square
    :target: https://pypi.python.org/pypi/sqlalchemy-datatables/

.. |Code Quality| image:: https://img.shields.io/scrutinizer/g/Pegase745/sqlalchemy-datatables.svg?style=flat-square
    :target: https://scrutinizer-ci.com/g/Pegase745/sqlalchemy-datatables

.. |Coveralls| image:: https://img.shields.io/coveralls/Pegase745/sqlalchemy-datatables.svg?style=flat-square
    :target: https://coveralls.io/r/Pegase745/sqlalchemy-datatables

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
        columns = []
        columns.append(ColumnDT('id'))
        columns.append(ColumnDT('name', filter=upper))
        columns.append(ColumnDT('address.description'))
        columns.append(ColumnDT('created_at'))

        # defining the initial query depending on your purpose
        query = DBSession.query(User).join(Address).filter(Address.id > 14)

        # instantiating a DataTable for the query and table needed
        rowTable = DataTables(request.GET, User, query, columns)

        # returns what is needed by DataTable
        return rowTable.output_result()


You can find detailed working examples for Pyramid and Flask in the repository.

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