from __future__ import absolute_import

from collections import namedtuple

from datatables.search_methods import SEARCH_METHODS

NULLS_ORDER = ['nullsfirst', 'nullslast']

ColumnTuple = namedtuple('ColumnDT', [
    'sqla_expr',
    'column_name',
    'mData',
    'search_method',
    'nulls_order',
    'global_search',
])


class ColumnDT(ColumnTuple):
    """
    Define a DataTables column.

    :param sqla_expr: SQLAlchemy queryable attribute of object
    (column, column_property, hybrid property, or combined expression)
    :param mData: name of the mData property as defined in the
    DataTables javascript options (default None)
    :param search_method: Define how to interpret search values.
        Possible values:
            - 'none'
            - 'string_contains' (default)
            - 'ilike'
            - 'like'
            - 'numeric'
            - 'date'
            - 'yadcf_text'
            - 'yadcf_autocomplete'
            - 'yadcf_select'
            - 'yadcf_multi_select'
            - 'yadcf_range_number'
            - 'yadcf_range_number_slider'
            - 'yadcf_range_date'
    :param nulls_order: define a sort order for the NULL values.
        Possible values:
            - None (default)
            - 'nullsfirst'
            - 'nullslast'.
    :param global_search: search this column for the global search box

    :type sqla_expr: SQLAlchemy query expression
    :type mData: str
    :type search_method: str
    :type nulls_order: str
    :type global_search: bool

    :return: a ColumnDT object
    :rtype: ColumnDT
    """

    def __new__(
            cls,
            sqla_expr,
            column_name=None,
            mData=None,
            search_method='string_contains',
            nulls_order=None,
            global_search=True,
    ):
        """Set default values due to namedtuple immutability."""
        if nulls_order and nulls_order not in NULLS_ORDER:
            raise ValueError(
                '{} is not an allowed value for nulls_order.'.format(
                    nulls_order))

        if search_method not in SEARCH_METHODS:
            raise ValueError(
                '{} is not an allowed value for search_method.'.format(
                    search_method))

        return super(ColumnDT, cls).__new__(
            cls,
            sqla_expr,
            column_name,
            mData,
            search_method,
            nulls_order,
            global_search,
        )
