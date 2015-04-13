import os
import sys
import transaction
from time import sleep

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from ..models import (
    DBSession,
    User,
    Address,
    Base,
)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        i = 0
        while i < 30:
            address = Address(description='Address#2' + str(i).rjust(2, "0"))
            DBSession.add(address)
            user = User(name='User#1' + str(i).rjust(2, "0"))
            user.address = address
            DBSession.add(user)
            sleep(1)
            i += 1
