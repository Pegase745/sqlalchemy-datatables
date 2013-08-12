sqlalchemy-datatables [![Build Status](https://travis-ci.org/Pegase745/sqlalchemy-datatables.png?branch=master)](https://travis-ci.org/Pegase745/sqlalchemy-datatables)
=====================

## Usage
The package is available on [PyPI] (https://pypi.python.org/pypi/sqlalchemy-datatables/0.1.0)

> pip install sqlalchemy-datatables

## A simple example

**models.py**
```python
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    address = relationship("Address", uselist=False, backref="user")

    def __init__(self, name):
        self.name = name

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    description = Column(Text, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, description):
        self.description = description
```

**views.py**
```python
from .models import DBSession, User
from datatables import ColumnDT, DataTables

def _upper(chain):
    ret = chain.upper()
    if ret:
        return ret
    else:
        return chain

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    return {'project': 'test-project'}
    
@view_config(route_name='simple_example', request_method='GET', renderer='json')
def simple_example(request):
  # defining columns
  columns = []
  columns.append(ColumnDT('id'))
  columns.append(ColumnDT('name', None, _upper))
  columns.append(ColumnDT('address.description'))
  columns.append(ColumnDT('created_at', None , str))

  # defining the initial query depending on your purpose
  query = DBSession.query(User).join(Address).filter(Address.id > 14)

  # instantiating a DataTable for the query and table needed
  rowTable = DataTables(request, User, query, columns) 

  # returns what is needed by DataTable 
  return rowTable.output_result()
```

**templates/home.pt**
```html
<!--do your stuff-->
<table class="table" id="simple-example">
  <thead>
    <tr>
      <th>Id</th>
      <th>User name</th>
      <th>Address description</th>
      <th>Created at</th>
    </tr>
  </thead>
  <tbody></tbody>
</table>
<!--do your stuff-->
<script type="text/javascript" charset="utf-8">
  $(document).ready(function(){
    $('#simple-example').dataTable({
      "bProcessing": true,
      "bServerSide": true,
      "sAjaxSource": "${request.route_path('simple_example')}"
    });
  });
</script>
```

## Testing the Pyramid based ''test-project''
```shell
$ git clone 
$ virtualenv --no-site-packages sqlalchemy-datatables
$ cd sqlalchemy-datatables/
$ cd test-project/
$ $venv/bin/python setup.py develop

Once only: 
$ $venv/bin/python sqlalchemy-datatables/setup.py develop

$ $venv/bin/pserve development.ini
```

## License

Copyright (c) 2013 Michel Nemnom

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
