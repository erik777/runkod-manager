import socket

import os
from flask_restful import reqparse, Resource

from manager.util import assert_env_vars

assert_env_vars('MASTER_IP')

MASTER_IP = os.environ.get('MASTER_IP')


class HostIpResource(Resource):
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        parser.add_argument('host', type=str, required=True, location=['json', 'args'])
        args = parser.parse_args()

        host = args['host']

        try:
            ip = socket.gethostbyname(host)
            rv = {
                'ip': ip,
                'valid': (MASTER_IP == ip)
            }
        except BaseException:
            rv = {
                'valid': False
            }

        return rv
