from __future__ import absolute_import

import math

from sqlalchemy import Text, func, or_
from sqlalchemy.dialects import mysql, postgresql, sqlite

from datatables.clean_regex import clean_regex
from datatables.search_methods import SEARCH_METHODS


class DataTables:
    """Class defining a DataTables object.

    :param request: request containing the GET values, specified by the
        datatable for filtering, sorting and paging
    :type request: pyramid.request
    :param query: the query wanted to be seen in the the table
    :type query: sqlalchemy.orm.query.Query
    :param columns: columns specification for the datatables
    :type columns: list

    :returns: a DataTables object
    """

    def __init__(self, request, query, columns, allow_regex_searches=False):
        """Initialize object and run the query."""
        self.params = dict(request)
        if 'sEcho' in self.params:
            raise ValueError(
                'Legacy datatables not supported, upgrade to >=1.10')
        self.query = query
        self.columns = columns
        self.results = None
        self.allow_regex_searches = allow_regex_searches

        # total in the table after filtering
        self.cardinality_filtered = 0

        # total in the table unfiltered
        self.cardinality = 0

        self.yadcf_params = []
        self.filter_expressions = []
        self.error = None
        try:
            self.run()
        except Exception as exc:
            self.error = str(exc)

    def output_result(self):
        """Output results in the format needed by DataTables."""
        output = {}
        output['draw'] = str(int(self.params.get('draw', 1)))
        output['recordsTotal'] = str(self.cardinality)
        output['recordsFiltered'] = str(self.cardinality_filtered)
        if self.error:
            output['error'] = self.error
            return output

        output['data'] = self.results
        for k, v in self.yadcf_params:
            output[k] = v
        return output

    def _query_with_all_filters_except_one(self, query, exclude):
        return query.filter(*[
            e for i, e in enumerate(self.filter_expressions)
            if e is not None and i is not exclude
        ])

    def _set_yadcf_data(self, query):
        # determine values for yadcf filters
        for i, col in enumerate(self.columns):
            if col.search_method in 'yadcf_range_number_slider':
                v = query.add_columns(
                    func.min(col.sqla_expr), func.max(col.sqla_expr)).one()
                self.yadcf_params.append(('yadcf_data_{:d}'.format(i),
                                          (math.floor(v[0]), math.ceil(v[1]))))
            if col.search_method in [
                    'yadcf_select', 'yadcf_multi_select', 'yadcf_autocomplete'
            ]:
                filtered = self._query_with_all_filters_except_one(
                    query=query, exclude=i)
                v = filtered.add_columns(col.sqla_expr).distinct().all()
                self.yadcf_params.append(('yadcf_data_{:d}'.format(i),
                                          [r[0] for r in v]))

    def run(self):
        """Launch filtering, sorting and paging to output results."""
        query = self.query

        # count before filtering
        self.cardinality = query.add_columns(self.columns[0].sqla_expr).count()

        self._set_column_filter_expressions()
        self._set_global_filter_expression()
        self._set_sort_expressions()
        self._set_yadcf_data(query)

        # apply filters
        query = query.filter(
            *[e for e in self.filter_expressions if e is not None])

        self.cardinality_filtered = query.add_columns(
            self.columns[0].sqla_expr).count()

        # apply sorts
        query = query.order_by(
            *[e for e in self.sort_expressions if e is not None])

        # add paging options
        length = int(self.params.get('length'))
        if length >= 0:
            query = query.limit(length)
        elif length == -1:
            pass
        else:
            raise (ValueError(
                'Length should be a positive integer or -1 to disable'))
        query = query.offset(int(self.params.get('start')))

        # add columns to query
        query = query.add_columns(*[c.sqla_expr for c in self.columns])

        # fetch the result of the queries
        column_names = [
            col.mData if col.mData else str(i)
            for i, col in enumerate(self.columns)
        ]
        self.results = [{k: v
                         for k, v in zip(column_names, row)}
                        for row in query.all()]

    def _set_column_filter_expressions(self):
        """Construct the query: filtering.

        Add filtering when per column searching is used.
        """
        # per columns filters:
        for i in range(len(self.columns)):
            filter_expr = None
            value = self.params.get('columns[{:d}][search][value]'.format(i),
                                    '')
            if value:
                search_func = SEARCH_METHODS[self.columns[i].search_method]
                filter_expr = search_func(self.columns[i].sqla_expr, value)
            self.filter_expressions.append(filter_expr)

    def _set_global_filter_expression(self):
        # global search filter
        global_search = self.params.get('search[value]', '')
        if global_search == '':
            return

        if (self.allow_regex_searches
                and self.params.get('search[regex]') == 'true'):
            op = self._get_regex_operator()
            val = clean_regex(global_search)

            def filter_for(col):
                return col.sqla_expr.op(op)(val)
        else:
            val = '%' + global_search + '%'

            def filter_for(col):
                return col.sqla_expr.cast(Text).ilike(val)

        global_filter = [
            filter_for(col) for col in self.columns if col.global_search
        ]

        self.filter_expressions.append(or_(*global_filter))

    def _set_sort_expressions(self):
        """Construct the query: sorting.

        Add sorting(ORDER BY) on the columns needed to be applied on.
        """
        sort_expressions = []
        i = 0
        while self.params.get('order[{:d}][column]'.format(i), False):
            column_nr = int(self.params.get('order[{:d}][column]'.format(i)))
            column = self.columns[column_nr]
            direction = self.params.get('order[{:d}][dir]'.format(i))
            sort_expr = column.sqla_expr
            if direction == 'asc':
                sort_expr = sort_expr.asc()
            elif direction == 'desc':
                sort_expr = sort_expr.desc()
            else:
                raise ValueError(
                    'Invalid order direction: {}'.format(direction))
            if column.nulls_order:
                if column.nulls_order == 'nullsfirst':
                    sort_expr = sort_expr.nullsfirst()
                elif column.nulls_order == 'nullslast':
                    sort_expr = sort_expr.nullslast()
                else:
                    raise ValueError(
                        'Invalid order direction: {}'.format(direction))

            sort_expressions.append(sort_expr)
            i += 1
        self.sort_expressions = sort_expressions

    def _get_regex_operator(self):
        if isinstance(self.query.session.bind.dialect, postgresql.dialect):
            return '~'
        elif isinstance(self.query.session.bind.dialect, mysql.dialect):
            return 'REGEXP'
        elif isinstance(self.query.session.bind.dialect, sqlite.dialect):
            return 'REGEXP'
        else:
            raise NotImplementedError(
                'Regex searches are not implemented for this dialect')
