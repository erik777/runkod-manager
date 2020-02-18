from datetime import timedelta

from flask_restful import reqparse, Resource, abort

from manager.constants import *
from manager.db import session_maker
from manager.model import Project
from manager.util import dt_api_format


class ProjectResource(Resource):
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        parser.add_argument('name', type=str, required=True, location=['json', 'args'])
        args = parser.parse_args()

        name = args['name']

        session = session_maker()
        project: Project = session.query(Project).filter(Project.name == name).first()
        session.close()

        if project is None:
            abort(404)

        next_cert_date = None
        if project.cert_date:
            next_cert_date = project.cert_date + timedelta(days=SSL_RENEW_DATES)

        return {
                   'ip_errs': project.ip_errs,
                   'ips_resolved': project.ips_resolved.split(',') if project.ips_resolved is not None else [],
                   'next_ip_check': dt_api_format(project.next_ip_check),
                   'stopped': project.stopped,
                   'cert_status': project.cert_status,
                   'cert_date': dt_api_format(project.cert_date),
                   'next_cert_date': dt_api_format(next_cert_date)
               }, 200
