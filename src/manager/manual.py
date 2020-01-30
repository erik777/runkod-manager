from manager.db import session_maker
from manager.logger import create_logger
from manager.model import Project
from manager.util import now_utc

logger = create_logger('manual')


def reset_project():
    project_name = input('Project name: ').strip()

    session = session_maker()

    project: Project = session.query(Project).filter(Project.name == project_name).first()

    if project is None:
        session.close()
        logger.error('Project not found!')
        exit(1)

    project.ip_errs = 0
    project.next_ip_check = now_utc()
    project.stopped = 0
    project.cert_status = 0

    session.commit()

    logger.info("Done")
