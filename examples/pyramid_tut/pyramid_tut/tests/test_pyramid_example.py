import os
import sys
import unittest
from datetime import date

import transaction
import webtest

from ..models import Base, User, DBSession, Address


class FunctionalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        from .. import main

        settings = {
            "sqlalchemy.url": "sqlite://",
            "auth.secret": "seekrit",
        }
        app = main({}, **settings)
        cls.testapp = webtest.TestApp(app)
        cls.dbsession = DBSession()
        cls.engine = cls.dbsession.bind
        Base.metadata.create_all(bind=cls.engine)

        for i in range(30):
            with transaction.manager:
                address = Address(description="Address#2" + str(i).rjust(2, "0"))

                cls.dbsession.add(address)

                user = User(
                    name="User#1" + str(i).rjust(2, "0"),
                    birthday=date(1980 + i % 8, i % 12 + 1, i % 10 + 1),
                )

                user.address = address

                cls.dbsession.add(user)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=cls.engine)

    def test_nr_of_users_in_db(self):
        nr_of_users_in_db = self.dbsession.query(User).count()
        self.assertEqual(nr_of_users_in_db, 30)

    def test_home(self):
        res = self.testapp.get("/")
        self.assertIn("Alchemy Scaffold for The Pyramid Web Framework", res.text)

    def test_home2(self):
        res = self.testapp.get("/")
        self.assertIn("Alchemy Scaffold for The Pyramid Web Framework", res.text)

    def test_home3(self):
        res = self.testapp.get("/dt_110x_advanced_column_search")
        self.assertIn("Alchemy Scaffold for The Pyramid Web Framework", res.text)
