import pytest

from datatables import ColumnDT

from .models import User


def test_init_with_default_params():
    """Return column with given default params."""
    col = ColumnDT(User.id)

    if not (col.nulls_order is None or col.search_method == 'string_contains'):
        raise AssertionError()


def test_with_filter_ok():
    """Return column with a specific filter."""
    col = ColumnDT(User.name, search_method='like')

    if col.search_method != 'like':
        raise AssertionError()


def test_with_valid_nulls_order():
    """Return column with a specific filter."""
    col = ColumnDT(User.name, nulls_order='nullslast')

    if col.nulls_order != 'nullslast':
        raise AssertionError()


def test_with_invalid_nulls_order():
    """Return column with a specific filter."""
    with pytest.raises(ValueError):
        ColumnDT(User.name, nulls_order='invalid')


def test_with_invalid_search_method():
    """Return column with a specific filter."""
    with pytest.raises(ValueError):
        ColumnDT(User.name, search_method='invalid')
