from unittest import TestCase

import pytest

from datatables import ColumnDT

from .models import User


class ColumnDTTest(TestCase):
    def test_init_with_default_params(self):
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
        with pytest.raises(ValueError):
            ColumnDT(User.name, nulls_order='invalid')

    def test_with_invalid_search_method(self):
        """Return column with a specific filter."""
        with pytest.raises(ValueError):
            ColumnDT(User.name, search_method='invalid')
