import os
import socket
from datetime import timedelta
from typing import List

from sqlalchemy.orm.session import Session

from manager.db import session_maker
from manager.helper import create_cert
from manager.logger import create_logger
from manager.model import Domain
from manager.util import now_utc

logger = create_logger('sync')

MASTER_IP = os.environ.get('MASTER_IP')


def next_try_date(domain: Domain):
    return (now_utc() + timedelta(minutes=1)) if domain.ip_errs <= 60 else (now_utc() + timedelta(minutes=15))


def checker():
    session: Session = session_maker()

    domains: List[Domain] = session.query(Domain) \
        .filter(Domain.stopped == 0) \
        .filter(Domain.next_ip_check < now_utc()).all()

    for domain in domains:
        # stop website after 700 ip errors (roughly 1 week of try)
        if domain.ip_errs >= 700:
            logger.info('Domain stopping {}'.format(domain.name))
            domain.stopped = 1
            domain.cert_status = 0
            domain.cert_file = None
            domain.cert_key_file = None
            domain.cert_date = None
            continue

        try:
            ip = socket.gethostbyname(domain.name)
        except BaseException:
            ip = None

        ip_verified = ip == MASTER_IP

        if ip_verified:
            domain.ip_errs = 0

            # refresh certs every 30 days
            if domain.cert_status == 1 and (now_utc() - domain.cert_date).days >= 30:
                if create_cert(domain.name):
                    domain.cert_date = now_utc()
                    domain.cert_file = ""
                    domain.cert_key_file = ""
                    logger.info('Domain certificate renewed {}'.format(domain.name))

            # first cert creation
            if domain.cert_status == 0:
                if create_cert(domain.name):
                    domain.cert_status = 1
                    domain.cert_date = now_utc()
                    domain.cert_file = ""
                    domain.cert_key_file = ""
                    logger.info('Domain certificate created {}'.format(domain.name))

        else:
            domain.next_ip_check = next_try_date(domain)
            domain.ip_errs += 1

    session.commit()
    session.close()
