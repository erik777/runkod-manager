import logging
import os
import socket
import time
from typing import List

from manager.cert import create_cert, delete_cert
from manager.db import session_maker
from manager.model import Domain
from manager.util import now_utc, in_15_min, in_1_min

logging.basicConfig(level=logging.INFO)

MASTER_IP = os.environ.get('MASTER_IP')


def next_try_date(domain: Domain):
    return in_1_min() if domain.ip_err_count <= 60 else in_15_min()


def checker():
    session = session_maker()

    domains: List[Domain] = session.query(Domain) \
        .filter(Domain.stopped == 0) \
        .filter(Domain.next_check < now_utc()).all()

    for domain in domains:
        # stop website after 700 ip errors (roughly 1 week of try)
        if domain.ip_err_count >= 700:
            delete_cert(domain.name)
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
        else:
            domain.next_check = next_try_date(domain)
            domain.ip_err_count += 1

    session.commit()
    session.close()


def main():
    while True:
        checker()
        time.sleep(4)
