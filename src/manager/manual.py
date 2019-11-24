from manager.db import session_maker
from manager.logger import create_logger
from manager.model import Domain
from manager.util import now_utc

logger = create_logger('manual')


def reset_domain():
    domain_name = input('Domain name: ').strip()

    session = session_maker()

    domain: Domain = session.query(Domain).filter(Domain.name == domain_name).first()

    if domain is None:
        session.close()
        logger.error('Project not found!')
        exit(1)

    domain.ip_errs = 0
    domain.next_ip_check = now_utc()
    domain.stopped = 0
    domain.cert_status = 0

    session.commit()

    logger.info("Done")
