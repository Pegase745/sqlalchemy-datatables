#!/usr/bin/env python
from setuptools import setup, find_packages

import sys

if sys.version_info<= (2,7):
    f = open('datatables/__init__.py', 'rb')
else:
    f = open('datatables/__init__.py', 'rb', encoding="utf-8")


__VERSION__ = [line for line in f \
    if line.startswith('__VERSION__')][0].split(\
    '=')[1].strip().lstrip('\'').rstrip('\'')


setup(
    name='sqlalchemy-datatables',
    version=__VERSION__,
    description='SQLAlchemy integration of jQuery DataTables',
    long_description=open('README.rst').read(),
    license='MIT',
    keywords='sqlalchemy datatables jquery pyramid',
    author='Michel Nemnom',
    author_email='michel.nemnom+pypi@gmail.com',
    url='https://github.com/pegase745/sqlalchemy-datatables',
    packages=find_packages(exclude=['test_app']),
    include_package_data=True,
    zip_safe=False,
    install_requires=['sqlalchemy'],
    py_modules=['datatables'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Pyramid',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)