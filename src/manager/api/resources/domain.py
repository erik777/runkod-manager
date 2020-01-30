from dns.resolver import Resolver, NXDOMAIN, NoAnswer
from flask_restful import reqparse, Resource
from sqlalchemy.orm.session import Session

from manager.db import session_maker
from manager.model import Domain

resolver = Resolver()


class DomainKeyResource(Resource):
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        parser.add_argument('domain', type=str, required=True, location=['json', 'args'])
        args = parser.parse_args()

        domain = args['domain']

        try:
            resolver.query(domain, 'TXT')
        except NoAnswer:
            pass
        except NXDOMAIN:
            rv = {
                'status': 2,
                'msg': 'Not a valid domain name'
            }

            return rv, 406

        session: Session = session_maker()

        rec: Domain = session.query(Domain).filter(Domain.name == domain).first()

        if rec is None:
            rec = Domain(domain)
            session.add(rec)
            session.commit()

        rv = {
            'status': 1,
            'key': rec.key
        }

        return rv, 200
