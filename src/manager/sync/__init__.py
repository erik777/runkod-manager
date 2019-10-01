from manager.constants import *
from manager.db import mongo_db
from manager.db import session_maker
from manager.db_helper import set_project_since_time, get_project_since_time
from manager.logger import create_logger
from manager.model import Domain

logger = create_logger('sync')


def get_project_list(since=None) -> list:
    filters = {'radiksType': 'project', 'custom': True}
    if since:
        filters['updatedAt'] = {"$gt": since}
    projects = mongo_db['radiks-server-data'].find(filters, sort=[('updatedAt', 1)])
    return [x for x in projects]


def sync():
    session = session_maker()

    since = get_project_since_time(session)
    projects = get_project_list(since)

    if len(projects) == 0:
        session.close()
        return

    for project in projects:
        if project['status'] == PROJECT_STATUS_ON and session.query(Domain).filter(
                Domain.name == project['name']).first() is None:
            d = Domain()
            d.name = project['name']
            session.add(d)

            logger.info('New project {}'.format(project['name']))

        set_project_since_time(session, project['updatedAt'])
        session.flush()

    session.commit()
    session.close()
