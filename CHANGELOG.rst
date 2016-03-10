Change log
==========

All notable changes to this project will be documented in this file.
This project adheres to `Semantic Versioning <http://semver.org/>`_ and `Keep A Changelog <http://keepachangelog.com/>`_.

Unreleased_
-----------
Added
~~~~~
  - Allow filtering based on row data (`filterarg` param in ColumnDT).
  - Add CHANGELOG.

Fixed
~~~~~
  - Fix cell's filter function to run only once.

0.2.1_ - 2016-01-08
-------------------
Fixed
~~~~~
  - Fix fields with a None value that should not be filtered if column search is empty.
  - Fix bug when sort is done on first column.

0.2.0_ - 2015-12-06
-------------------
Added
~~~~~
  - Add DataTables > 1.10.x compatibility.
  - Ensure backward compatibility with DataTables <= 1.9.x.
  - Add unit tests.
  - Add Pyramid and Flask examples.

Changed
~~~~~~~
  - Follow Semantic versioning now.

0.1.7_ - 2015-08-27
-------------------
Added
~~~~~
  - Allow lists to be printed as well on relationships, not just one to one.
  - Properly type request values for python 3.4.
  - Work with python 3.4.
  - Explicit imports.
  - Override searchability server side.
  - Sort by relationships of relationships.
  - Add MANIFEST.
  - Add coverage test with Coveralls.

Changed
~~~~~~~
  - Change sorting algorithm to rely solely on SQLAlchemy to do the joining.

Fixed
~~~~~
  - Fix to unicode problem in python 2.7.
  - Fix searches per column, simplified example, updated js.

0.1.6_ - 2015-08-27
-------------------
Added
~~~~~
  - Allow to run with python 3.x.

Removed
~~~~~~~
  - Remove python 2.5 from Travis.

Fixed
~~~~~
  - Fix unicode problem in python 3.2.

0.1.5_ - 2013-10-18
-------------------
Added
~~~~~
  - Add awareness of bSearchable_* properties, while doing a global search.

Fixed
~~~~~
  - Fix bug when searching Id columns.
  - Fix bug when showing in ColumnDT, an SQLAlchemy's @hybrid_property or a Python @property.

0.1.4_ - 2013-09-17
-------------------
Added
~~~~~
  - Add searching individual columns, with `like` possibilities.

0.1.3_ - 2013-09-16
-------------------
Fixed
~~~~~
  - Fix setup.py's README error on develop.

0.1.2_ - 2015-08-27
-------------------
Fixed
~~~~~
  - Fix filtering and sorting errors due to relationships.
  - Fix filter's default value to `str` in order to avoid JSON serializable type errors.

0.1.1_ - 2013-08-12
-------------------
Fixed
~~~~~
  - Fix showing columns issuing from relations.

0.1.0_ - 2013-08-11
-------------------
Added
~~~~~
  - Initial version of the lib.

.. _Unreleased: https://github.com/Pegase745/sqlalchemy-datatables/compare/v0.2.1...master
.. _0.2.1: https://github.com/Pegase745/sqlalchemy-datatables/compare/v0.2.0...v0.2.1
.. _0.2.0: https://github.com/Pegase745/sqlalchemy-datatables/compare/v0.1.7...v0.2.0
.. _0.1.7: https://github.com/Pegase745/sqlalchemy-datatables/compare/v0.1.6...v0.1.7
.. _0.1.6: https://github.com/Pegase745/sqlalchemy-datatables/compare/v0.1.5...v0.1.6
.. _0.1.5: https://github.com/Pegase745/sqlalchemy-datatables/compare/v0.1.4...v0.1.5
.. _0.1.4: https://github.com/Pegase745/sqlalchemy-datatables/compare/v0.1.2...v0.1.4
.. _0.1.2: https://github.com/Pegase745/sqlalchemy-datatables/compare/v0.1.1...v0.1.2
.. _0.1.1: https://github.com/Pegase745/sqlalchemy-datatables/compare/v0.1.0...v0.1.1
.. _0.1.0: https://github.com/Pegase745/sqlalchemy-datatables/compare/v0.1.0...v0.1.0