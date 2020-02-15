import argparse
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)

assert sys.version_info[0] == 3 and sys.version_info[1] >= 6, 'Requires Python 3.6 or newer'

os.sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from manager.util import assert_env_vars

assert_env_vars('MONGO_URI', 'LOCAL_DB_URI')


def main():
    parser = argparse.ArgumentParser(description='')
    cmd_list = (
        'sync',
        'project_checker',
        'domain_cleaner',
        'config_writer',
        'worker',
        'api',
        'reset_project',
        'create_db',
        'create_data',
        'drop_db',
    )

    parser.add_argument('cmd', choices=cmd_list, nargs='?', default='app')
    parser.add_argument('--force', default=0)

    args = parser.parse_args()
    cmd = args.cmd

    if cmd == 'sync':
        from manager.sync import sync
        sync()

    if cmd == 'project_checker':
        from manager.project_checker import project_checker
        project_checker()

    if cmd == 'domain_cleaner':
        from manager.domain_cleaner import domain_cleaner
        domain_cleaner()

    if cmd == 'config_writer':
        from manager.config_writer import writer
        writer(args.force)

    if cmd == 'worker':
        from manager.worker import main
        main()

    if cmd == 'api':
        from manager.api.app import main
        main()

    if cmd == 'reset_project':
        from manager.manual import reset_project
        reset_project()

    if cmd == 'create_db':
        from manager.db_tool import create_db
        create_db()

    if cmd == 'create_data':
        from manager.db_tool import create_data
        create_data()

    if cmd == 'drop_db':
        from manager.db_tool import drop_db
        drop_db()


if __name__ == '__main__':
    main()
