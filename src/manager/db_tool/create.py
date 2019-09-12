import logging

from manager.db import local_db_engine, session_maker
from manager.model import *

logging.basicConfig(level=logging.INFO)


def create_db():
    Base.metadata.create_all(bind=local_db_engine)
    logging.info("OK")


def create_data():
    session = session_maker()

    s = State()
    s.id = 'default'

    session.add(s)
    session.commit()


if __name__ == "__main__":
    create_db()
