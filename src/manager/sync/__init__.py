from manager.constants import *
from manager.db import mongo_db
from manager.db import session_maker
from manager.db_helper import set_project_since_time, get_project_since_time
from manager.helper import delete_cert
from manager.logger import create_logger
from manager.model import Domain

logger = create_logger('sync')


def get_project_list(since=None) -> list:
    filters = {'radiksType': 'project', 'custom': True}
    if since:
        filters['updatedAt'] = {"$lt": since}
    projects = mongo_db['radiks-server-data'].find(filters, sort=[('updatedAt', 1)])
    return [x for x in projects]


def sync():
    session = session_maker()

    since_time = get_project_since_time(session)

    projects = get_project_list(since_time)

    if len(projects) == 0:
        session.close()
        return

    for project in projects:
        if project['status'] == PROJECT_STATUS_ON:
            d = Domain()
            d.name = project['name']
            session.add(d)

            logger.info('New project {}'.format(project['name']))

        if project['status'] == PROJECT_STATUS_DELETED:
            logger.info('Project deleted {}'.format(project['name']))

            d = session.query(Domain).filter(Domain.name == project['name'])

            if d is not None:
                logger.info('Project deleting {}'.format(project['name']))
                session.delete(d)
                logger.info('Record deleted {}'.format(project['name']))
                delete_cert(project['name'])
                logger.info('Certificate deleted {}'.format(project['name']))
            else:
                logger.info('Record not found {}'.format(project['name']))

        set_project_since_time(session, project['updatedAt'])
        session.flush()

    session.commit()
