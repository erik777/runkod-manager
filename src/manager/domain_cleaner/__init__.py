from datetime import timedelta
from typing import List

from sqlalchemy.orm.session import Session

from manager.db import session_maker
from manager.logger import create_logger
from manager.model import Project, Domain
from manager.util import now_utc

logger = create_logger('domain-cleaner')


def domain_cleaner():
    session: Session = session_maker()

    min_date = now_utc() - timedelta(hours=24)

    domains: List[Domain] = session.query(Domain) \
        .filter(Domain.verified == 0) \
        .filter(Project.created < min_date).all()

    if len(domains) == 0:
        session.close()
        return

    for dom in domains:
        session.delete(dom)
        logger.info('Domain deleted {}'.format(dom.name))

    session.commit()
    session.close()
