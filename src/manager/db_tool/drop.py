import logging
import sys

from manager.db import local_db_engine
from manager.model import *

logging.basicConfig(level=logging.INFO)


def drop_db(warn=True):
    if warn:
        confirm = input('All data will be deleted. Are you sure? Y or N: ')

        while confirm not in ['Y', 'N']:
            confirm = input('Y or N: ')

        if confirm == 'N':
            logging.info('Aborting.')
            sys.exit(0)

    Base.metadata.drop_all(bind=local_db_engine)
    logging.info("OK")


if __name__ == "__main__":
    drop_db()
