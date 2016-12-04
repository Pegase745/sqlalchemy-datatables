"""Main entry file, definition of ColumnDT and DataTables."""
import sys
from collections import namedtuple
from logging import getLogger
from dateutil.parser import parse as date_parse
import datetime
from sqlalchemy.dialects import postgresql, mysql, sqlite
from sqlalchemy import func, Text, or_

log = getLogger(__file__)

if sys.version_info > (3, 0):
    unicode = str


def clean_regex(regex):
    '''
    escape any regex special characters other than alternation |

    :param regex: regex from datatables interface
    :type regex: str
    :rtype: str with regex to use with database
    '''
    # copy for return
    ret_regex = regex

    # these characters are escaped (all except alternation | and escape \)
    # see http://www.regular-expressions.info/refquick.html
    escape_chars = '[^$.?*+(){}'

    # remove any escape chars
    ret_regex = ret_regex.replace('\\', '')

    # escape any characters which are used by regex
    # could probably concoct something incomprehensible using re.sub() but
    # prefer to write clear code with this loop
    # note expectation that no characters have already been escaped
    for c in escape_chars:
        ret_regex = ret_regex.replace(c, '\\' + c)

    # remove any double alternations until these don't exist any more
    while True:
        old_regex = ret_regex
        ret_regex = ret_regex.replace('||', '|')
        if old_regex == ret_regex:
            break

    # if last char is alternation | remove it because this
    # will cause operational error
    # this can happen as user is typing in global search box
    while len(ret_regex) >= 1 and ret_regex[-1] == '|':
        ret_regex = ret_regex[:-1]

    # and back to the caller
    return ret_regex


search_operators = {
    '=': lambda expr, value: expr == value,
    '>': lambda expr, value: expr > value,
    '>=': lambda expr, value: expr >= value,
    '<': lambda expr, value: expr < value,
    '<=': lambda expr, value: expr <= value,
}


def parse_query_value(combined_value):
    """Parse value in form of '>value' to a lambda and a value."""

    split = len(combined_value) - len(combined_value.lstrip('<>='))
    operator = combined_value[:split]
    if operator == '':
        operator = '='
    try:
        operator_func = search_operators[operator]
    except KeyError:
        raise ValueError(
            'Numeric query should start with operator, choose from %s'
            % ', '.join(search_operators.keys()))
    value = combined_value[split:].strip()
    return operator_func, value


def numeric_query(expr, value):
    operator_func, value = parse_query_value(value)
    if value == '':
        num_value = 0
    else:
        num_value = float(value)

    return operator_func(expr, num_value)


def date_query(expr, value):
    operator_func, value = parse_query_value(value)
    try:
        date_value = date_parse(value)
    except ValueError:
        date_value = datetime.datetime.now()

    return operator_func(expr, date_value)


def yadcf_range_number(expr, value):
    v_from, v_to = value.split('-yadcf_delim-')
    v_from = float(v_from) if v_from != '' else -float('inf')
    v_to = float(v_to) if v_to != '' else float('inf')
    log.debug('yadcf_range_number: between %f and %f', v_from, v_to)
    return expr.between(v_from, v_to)


def yadcf_range_date(expr, value):
    v_from, v_to = value.split('-yadcf_delim-')
    v_from = date_parse(v_from) if v_from != '' else datetime.date.min
    v_to = date_parse(v_to) if v_to != '' else datetime.date.max
    log.debug('yadcf_range_date: between %s and %s', v_from, v_to)
    return expr.between(v_from, v_to)


def yadcf_multi_select(expr, value):
    options = value.split('|')
    log.debug('yadcf_multi_select: in %s', options)
    return expr.cast(Text).in_(options)


search_methods = {
    'none': {
        'to_query': lambda expr, value: None,
    },
    'string_contains': {
        'to_query': lambda expr, value: expr.ilike('%' + value + '%'),
    },
    'ilike': {
        'to_query': lambda expr, value: expr.ilike(value),
    },
    'like': {
        'to_query': lambda expr, value: expr.like(value),
    },
    'numeric': {
        'to_query': numeric_query,
    },
    'date': {
        'to_query': date_query,
    },
    'yadcf_text': {
        'to_query': lambda expr, value: expr.ilike('%' + value + '%'),
    },
    'yadcf_autocomplete': {
        'to_query': lambda expr, value: expr == value,
    },
    'yadcf_select': {
        'to_query': lambda expr, value: expr.ilike('%' + value + '%'),
    },
    'yadcf_multi_select': {
        'to_query': yadcf_multi_select,
    },
    'yadcf_range_number': {
        'to_query': yadcf_range_number,
    },
    'yadcf_range_number_slider': {
        'to_query': yadcf_range_number,
    },
    'yadcf_range_date': {
        'to_query': yadcf_range_date,
    },
}


ColumnTuple = namedtuple(
    'ColumnDT',
    ['sqla_expr', 'column_name', 'mData', 'search_method',
     'nulls_order', 'global_search'])


class InvalidParameter(Exception):

    """Class defining an invalid parameter exception."""

    pass


class ColumnDT(ColumnTuple):

    """Class defining a DataTables Column with a ColumnTuple.

    :param sqla_expr: SQLAlchemy queryable attribute of object
        (column, column_property, hubrid property, or
        combined expression)
    :type sqla_expr: ?
    :param mData: name of the mData property as defined in the
        DataTables javascript options (default None)
    :type mData: str
    :param search_method: Define how to interpret search values.
        Possible values: 'none', 'contains', 'ilike', 'like',
        'numeric'
    :type search_method: str
    :param nulls_order: define a sort order for the NULL values. Possible
        values: nullsfirst, nullslast. (default None)
    :type nulls_order: str
    :param global_search: search this column for the global search box
    :type global_search: bool
    :returns: a ColumnDT object
    """

    def __new__(cls, sqla_expr, column_name=None, mData=None,
                search_method='string_contains', nulls_order=None,
                global_search=True):
        """Set default values for mData and filter.

        On creation, sets default None values for mData and string value for
        filter (cause: Object representation is not JSON serializable).
        """
        # check if allowed value
        if nulls_order and nulls_order not in ['nullsfirst', 'nullslast']:
            raise ValueError('`%s` is not an allowed value for nulls_order.'
                             % nulls_order)
        if search_method not in search_methods:
            raise ValueError('`%s` is not an allowed value for search_method.'
                             % search_method)

        return super(ColumnDT, cls).__new__(
            cls, sqla_expr, column_name, mData, search_method,
            nulls_order, global_search)


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

    def __init__(self, request, query, columns,
                 allow_regex_searches=False):
        """Initialize object and run the query."""
        self.params = dict(request)
        if 'sEcho' in self.params:
            raise ValueError(
                'Legace datatables not supported, upgrade to >=1.10')
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
        self.run()

    def output_result(self):
        """Output results in the format needed by DataTables."""
        output = {}
        output['draw'] = str(int(self.params['draw']))
        output['recordsTotal'] = str(self.cardinality)
        output['recordsFiltered'] = str(self.cardinality_filtered)
        output['data'] = self.results
        for k, v in self.yadcf_params:
            output[k] = v
        return output

    def _query_with_all_filters_except_one(self, query, exclude):
        return query.filter(
            *[e for i, e in enumerate(self.filter_expressions)
              if e is not None and i is not exclude]
        )

    def _set_yadcf_data(self, query):
        # determine values for yadcf filters
        for i, col in enumerate(self.columns):
            if col.search_method in 'yadcf_range_number_slider':
                v = query.add_columns(
                    func.floor(func.min(col.sqla_expr)),
                    func.ceil(func.max(col.sqla_expr))
                ).one()
                self.yadcf_params.append(
                    ('yadcf_data_{:d}'.format(i), v))
            if col.search_method in ['yadcf_select', 'yadcf_multi_select',
                                     'yadcf_autocomplete']:
                filtered = self._query_with_all_filters_except_one(
                    query=query, exclude=i)
                v = filtered.add_columns(col.sqla_expr).distinct().all()
                self.yadcf_params.append(
                    ('yadcf_data_{:d}'.format(i), [r[0] for r in v]))

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
        query = query.limit(int(self.params.get('length')))
        query = query.offset(int(self.params.get('start')))

        # add columns to query
        query = query.add_columns(
            *[c.sqla_expr for c in self.columns])

        # fetch the result of the queries
        column_names = [col.mData if col.mData else str(i)
                        for i, col in enumerate(self.columns)]
        self.results = [{k: v for k, v in zip(
            column_names, row)} for row in query.all()]

    def _set_column_filter_expressions(self):
        """Construct the query: filtering.

        Add filtering when per column searching is used
        """

        # per columns filters:
        for i in range(len(self.columns)):
            filter_expr = None
            value = self.params.get(
                'columns[{:d}][search][value]'.format(i), '')
            if value:
                search_func = search_methods[
                    self.columns[i].search_method]['to_query']
                filter_expr = search_func(self.columns[i].sqla_expr, value)
            self.filter_expressions.append(filter_expr)

    def _set_global_filter_expression(self):
        # global search filter
        global_search = self.params.get('search[value]', '')
        if global_search is '':
            return

        if (self.allow_regex_searches and
                self.params.get('search[regex]') == 'true'):
            op = self._get_regex_operator()
            val = clean_regex(global_search)
            filter_for = lambda col: col.sqla_expr.op(op)(val)
        else:
            val = '%' + global_search + '%'
            filter_for = lambda col: col.sqla_expr.cast(Text).ilike(val)

        global_filter = [filter_for(col)
                         for col in self.columns if col.global_search]

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
                        'Invalid order direction: %s'.format(direction))

            sort_expressions.append(sort_expr)
            i += 1
        self.sort_expressions = sort_expressions

    def _get_regex_operator(self):
        if isinstance(
                self.query.session.bind.dialect,
                postgresql.dialect):
            return '~'
        elif isinstance(
                self.query.session.bind.dialect,
                mysql.dialect):
            return 'REGEXP'
        elif isinstance(
                self.query.session.bind.dialect,
                sqlite.dialect):
            return 'REGEXP'
        else:
            raise NotImplementedError(
                'Regex searches are not implemented for this dialect')
