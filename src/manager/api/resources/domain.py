from dns.resolver import Resolver
from flask_restful import reqparse, Resource
from sqlalchemy.orm.session import Session

from manager.db import session_maker
from manager.dns_helper import is_domain_exists, get_txt_records
from manager.model import Domain
from manager.util import now_utc

resolver = Resolver()


class DomainKeyResource(Resource):
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        parser.add_argument('name', type=str, required=True, location=['json', 'args'])
        args = parser.parse_args()

        name = args['name']

        if not is_domain_exists(name):
            rv = {
                'status': 2,
                'msg': 'Not a valid domain name'
            }

            return rv, 406

        session: Session = session_maker()

        rec: Domain = session.query(Domain).filter(Domain.name == name).first()

        if rec is None:
            rec = Domain(name)
            session.add(rec)
            session.commit()

        rv = {
            'status': 1,
            'msg': 'ok',
            'key': rec.key
        }

        session.close()

        return rv, 200


class DomainKeyCheckResource(Resource):
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        parser.add_argument('name', type=str, required=True, location=['json', 'args'])
        args = parser.parse_args()

        name = args['name']

        session: Session = session_maker()

        rec: Domain = session.query(Domain).filter(Domain.name == name).first()

        if rec.verified == 1:
            rv = {
                'status': 1,
                'msg': 'ok'
            }

            return rv, 200

        if rec is None:
            rv = {
                'status': 2,
                'msg': 'Domain record not found on database'
            }

            session.close()
            return rv, 406

        txt_records = get_txt_records(name)

        verified = rec.key in txt_records

        if not verified:
            rv = {
                'status': 3,
                'msg': 'Not verified'
            }

            session.close()
            return rv, 406

        rec.verified = 1
        rec.verification_date = now_utc()
        session.commit()
        session.close()

        rv = {
            'status': 1,
            'msg': 'ok'
        }

        return rv, 200
