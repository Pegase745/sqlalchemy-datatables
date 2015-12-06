"""Column DataTable unit tests."""
import unittest
from datatables import ColumnDT


class ColumnTest(unittest.TestCase):

    """Class defining a DataTables Column test plan."""

    def test_with_default_params_ok(self):
        """Return column with given default params."""
        col = ColumnDT('id')

        assert col.column_name == 'id'
        assert col.filter(col.column_name) == 'id'

    def test_with_filter_ok(self):
        """Return column with a specific filter."""
        col = ColumnDT('id', filter=lambda x: 'HANDLE %s' % x)

        assert col.filter(col.column_name) == 'HANDLE id'
