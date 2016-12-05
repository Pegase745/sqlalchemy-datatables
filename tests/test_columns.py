"""Column DataTable unit tests."""
import unittest
from datatables import ColumnDT
from .models import User


class ColumnTest(unittest.TestCase):

    """Class defining a DataTables Column test plan."""

    def test_with_default_params_ok(self):
        """Return column with given default params."""
        col = ColumnDT(User.id)

        assert col.nulls_order is None
        assert col.search_method == 'string_contains'

    def test_with_filter_ok(self):
        """Return column with a specific filter."""
        col = ColumnDT(User.name, search_method='like')

        assert col.search_method == 'like'

    def test_with_valid_nulls_order(self):
        """Return column with a specific filter."""
        col = ColumnDT(User.name, nulls_order='nullslast')
        assert col.nulls_order == 'nullslast'

    def test_with_invalid_nulls_order(self):
        """Return column with a specific filter."""
        with self.assertRaises(ValueError):
            ColumnDT(User.name, nulls_order='invalid')

    def test_with_invalid_search_method(self):
        """Return column with a specific filter."""
        with self.assertRaises(ValueError):
            ColumnDT(User.name, search_method='invalid')
