import os
import socket
from datetime import timedelta
from typing import List

from sqlalchemy.orm.session import Session

from manager.helper import create_cert, delete_cert
from manager.db import session_maker
from manager.logger import create_logger
from manager.model import Domain
from manager.util import now_utc

logger = create_logger('sync')

MASTER_IP = os.environ.get('MASTER_IP')


def next_try_date(domain: Domain):
    return (now_utc() + timedelta(minutes=1)) if domain.ip_err_count <= 60 else (now_utc() + timedelta(minutes=15))


def checker():
    session: Session = session_maker()

    domains: List[Domain] = session.query(Domain) \
        .filter(Domain.stopped == 0) \
        .filter(Domain.next_check < now_utc()).all()

    for domain in domains:
        # stop website after 700 ip errors (roughly 1 week of try)
        if domain.ip_err_count >= 700:
            logger.info('Domain stopping {}'.format(domain.name))
            delete_cert(domain.name)
            logger.info('Domain cert deleted {}'.format(domain.name))
            domain.stopped = 1
            continue

        try:
            ip = socket.gethostbyname(domain.name)
        except BaseException:
            ip = None

        ip_verified = ip == MASTER_IP

        if ip_verified:
            domain.ip_err_count = 0

            if domain.cert == 0:
                if create_cert(domain.name):
                    domain.cert = 1
                    logger.info('Domain certificate created {}'.format(domain.name))
        else:
            domain.next_check = next_try_date(domain)
            domain.ip_err_count += 1

    session.commit()
    session.close()
