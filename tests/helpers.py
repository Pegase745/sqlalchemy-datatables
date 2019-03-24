def create_dt_params(columns, search='', start=0, length=10, order=None):
    """Create DataTables input parameters."""
    params = {
        'draw': '1',
        'start': str(start),
        'length': str(length),
        'search[value]': str(search),
        'search[regex]': 'false'
    }

    for i, item in enumerate(columns):
        cols = 'columns[%s]' % i
        params['%s%s' % (cols, '[data]')] = i
        params['%s%s' % (cols, '[name]')] = ''
        params['%s%s' % (cols, '[searchable]')] = 'true'
        params['%s%s' % (cols, '[orderable]')] = 'true'
        params['%s%s' % (cols, '[search][value]')] = ''
        params['%s%s' % (cols, '[search][regex]')] = 'false'

    for i, item in enumerate(order or [{'column': 0, 'dir': 'asc'}]):
        for key, value in item.items():
            params['order[%s][%s]' % (i, key)] = str(value)

    return params
