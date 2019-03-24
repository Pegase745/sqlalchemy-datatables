import datetime
import logging

from dateutil.parser import parse as date_parse
from sqlalchemy import Text

logger = logging.getLogger(__name__)

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
            'Numeric query should start with operator, choose from %s' %
            ', '.join(search_operators.keys()))
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
    logger.debug('yadcf_range_number: between %f and %f', v_from, v_to)
    return expr.between(v_from, v_to)


def yadcf_range_date(expr, value):
    v_from, v_to = value.split('-yadcf_delim-')
    v_from = date_parse(v_from) if v_from != '' else datetime.date.min
    v_to = date_parse(v_to) if v_to != '' else datetime.date.max
    logger.debug('yadcf_range_date: between %s and %s', v_from, v_to)
    return expr.between(v_from, v_to)


def yadcf_multi_select(expr, value):
    options = value.split('|')
    logger.debug('yadcf_multi_select: in %s', options)
    return expr.cast(Text).in_(options)


SEARCH_METHODS = {
    'none': lambda expr, value: None,
    'string_contains': lambda expr, value: expr.ilike('%' + value + '%'),
    'ilike': lambda expr, value: expr.ilike(value),
    'like': lambda expr, value: expr.like(value),
    'numeric': numeric_query,
    'date': date_query,
    'yadcf_text': lambda expr, value: expr.ilike('%' + value + '%'),
    'yadcf_autocomplete': lambda expr, value: expr == value,
    'yadcf_select': lambda expr, value: expr.ilike('%' + value + '%'),
    'yadcf_multi_select': yadcf_multi_select,
    'yadcf_range_number': yadcf_range_number,
    'yadcf_range_number_slider': yadcf_range_number,
    'yadcf_range_date': yadcf_range_date
}
