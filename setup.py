from setuptools import setup

__VERSION__ = '1.2.0'

setup(
    name='sqlalchemy-datatables',
    version=__VERSION__,
    description='SQLAlchemy integration of jQuery DataTables',
    long_description=open('README.rst').read(),
    license='MIT',
    keywords='sqlalchemy datatables jquery pyramid flask dt1.10',
    author='Michel Nemnom',
    author_email='michel.nemnom+pypi@gmail.com',
    url='https://github.com/pegase745/sqlalchemy-datatables',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'sqlalchemy',
        'python-dateutil',
    ],
    extras_require={
        'dev': [
            'faker',
            'flake8',
            'flake8-docstrings',
            'isort',
            'pytest',
            'pytest-cov',
            'yapf',
        ]
    },
    py_modules=['datatables'],
    test_suite='tests',
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
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])
