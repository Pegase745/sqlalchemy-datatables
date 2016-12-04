"""Column DataTable unit tests."""
import unittest
from datatables import ColumnDT
from .models import User


class ColumnTest(unittest.TestCase):

    """Class defining a DataTables Column test plan."""

    def test_with_default_params_ok(self):
        """Return column with given default params."""
        col = ColumnDT(User.id)

        assert col.nulls_order == None
        assert col.search_method == 'string_contains'

    def test_with_filter_ok(self):
        """Return column with a specific filter."""
        col = ColumnDT(User.name, search_method='like')

        assert col.search_method == 'like'
