from manager.db import mongo_db
from manager.constants import *
from manager.db import session_maker
from manager.model import Domain
from manager.db_helper import set_project_since_time, get_project_since_time
import logging

logging.basicConfig(level=logging.INFO)


def get_project_list(since=None) -> list:
    filters = {'radiksType': 'project', 'custom': True}
    if since:
        filters['updatedAt'] = {"$lt": since}
    projects = mongo_db['radiks-server-data'].find(filters, sort=[('updatedAt', 1)])
    return [x for x in projects]


def main():
    session = session_maker()

    since_time = get_project_since_time(session)

    projects = get_project_list(since_time)

    if len(projects) == 0:
        logging.info('No new project')
        session.close()
        return

    for project in projects:
        if project['status'] == PROJECT_STATUS_ON:
            # insert record to local db
            d = Domain()
            d.name = project['name']
            session.add(d)
            pass

        if project['status'] == PROJECT_STATUS_DELETED:
            # delete cert
            # delete record from local db
            pass

        set_project_since_time(session, project['updatedAt'])
        session.flush()

    session.commit()
