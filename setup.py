#!/usr/bin/env python
from setuptools import setup, find_packages

__VERSION__ = [line for line in file('datatables/__init__.py', 'rb') \
               if line.startswith('__VERSION__')][0].split(\
               '=')[1].strip().lstrip('\'').rstrip('\'')

setup(
    name='sqlalchemy-datatables',
    version=__VERSION__,
    description='SQLAlchemy integration of jQuery DataTables',
    long_description=open('README').read(),
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
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Pyramid',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)