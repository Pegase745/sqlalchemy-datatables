"""App configuration."""
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()

requires = [
    'Flask',
    'Jinja2',
    'Flask-SQLAlchemy',
]

setup(name='flask_tut',
      version='0.0',
      description='flask_tut',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg flask',
      packages=find_packages(),
      scripts=[
          'flask_tut/scripts/initializedb.py',
      ],
      include_package_data=True,
      zip_safe=False,
      test_suite='flask_tut',
      install_requires=requires,
      )
