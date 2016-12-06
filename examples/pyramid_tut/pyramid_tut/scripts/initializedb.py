"""Initialize DB with fixtures."""
import os
import sys
from datetime import date

import transaction
from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars
from sqlalchemy import engine_from_config

from ..models import Address, Base, DBSession, User


def usage(argv):
    """Help user on how to use the script."""
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    """Populate database with 30 users."""
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    for i in range(30):
        with transaction.manager:
            address = Address(description='Address#2' + str(i).rjust(2, "0"))
            DBSession.add(address)
            user = User(name='User#1' + str(i).rjust(2, "0"),
                        birthday=date(1980 + i % 8,
                                      i % 12 + 1,
                                      i % 10 + 1))
            user.address = address
            DBSession.add(user)
