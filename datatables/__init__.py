# -*- coding: utf-8 -*-
import sys

if sys.version_info > (3, 0):
    from datatables.datatables import ColumnDT, DataTables
else:
    from datatables import ColumnDT, DataTables


__VERSION__ = '0.1.7'
