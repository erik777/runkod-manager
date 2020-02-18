import os
import socket
from datetime import timedelta
from typing import List

from sqlalchemy.orm.session import Session

from manager.constants import SSL_RENEW_DATES
from manager.db import session_maker
from manager.dns_helper import get_a_records
from manager.helper import create_cert
from manager.logger import create_logger
from manager.model import Project
from manager.util import now_utc, assert_env_vars

assert_env_vars('MASTER_IP', 'CERT_BASE_DIR', 'LE_CERT_BASE_DIR', 'CERT_WEB_ROOT', 'CERT_EMAIL')

logger = create_logger('project-checker')

MASTER_IP = os.environ.get('MASTER_IP')


def next_try_date(project: Project):
    return (now_utc() + timedelta(minutes=1)) if project.ip_errs <= 60 else (now_utc() + timedelta(minutes=15))


def project_checker():
    session: Session = session_maker()

    projects: List[Project] = session.query(Project) \
        .filter(Project.stopped == 0) \
        .filter(Project.next_ip_check < now_utc()).all()

    for project in projects:
        # stop website after 700 ip errors (roughly 1 week of try)
        if project.ip_errs >= 700:
            logger.info('Project stopping {}'.format(project.name))
            project.stopped = 1
            project.cert_status = 0
            continue

        # Leaving here basic for future CNAME support scenario
        try:
            ip = socket.gethostbyname(project.name)
        except BaseException:
            ip = None

        ip_verified = ip == MASTER_IP

        # Save A record ip addresses
        project.ips_resolved = ','.join(get_a_records(project.name))

        if ip_verified:

            # renew certs every 30 days
            if project.cert_status == 1 and (now_utc() - project.cert_date).days >= SSL_RENEW_DATES:
                if create_cert(project):
                    project.cert_date = now_utc()
                    logger.info('Project certificate renewed {}'.format(project.name))

            # first cert creation
            if project.cert_status == 0:
                if create_cert(project):
                    project.cert_status = 1
                    project.cert_date = now_utc()
                    logger.info('Project certificate created {}'.format(project.name))

            # visit this project in 1 hour again
            project.next_ip_check = now_utc() + timedelta(minutes=60)
            project.ip_errs = 0
        else:
            project.next_ip_check = next_try_date(project)
            project.ip_errs += 1

    session.commit()
    session.close()
