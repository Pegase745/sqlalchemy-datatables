import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.rst")) as f:
    README = f.read()

setup(
    name="pyramid_tut",
    version="0.0",
    description="pyramid_tut",
    long_description=README,
    classifiers=[
        "Programming Language :: Python", "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
    ],
    author="",
    author_email="",
    url="",
    keywords="web wsgi bfg pylons pyramid",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite="pyramid_tut",
    install_requires=[],
    entry_points="""\
      [paste.app_factory]
      main = pyramid_tut:main
      [console_scripts]
      pyramid_tut_initdb = pyramid_tut.scripts.initializedb:main
      """)
