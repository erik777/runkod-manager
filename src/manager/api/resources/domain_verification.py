from dns.resolver import Resolver
from flask_restful import reqparse, Resource, abort
from sqlalchemy.orm.session import Session

from manager.db import session_maker, mongo_db
from manager.dns_helper import is_domain_exists, get_txt_records
from manager.model import Domain
from manager.util import now_utc

resolver = Resolver()


class DomainVerificationResource(Resource):

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        parser.add_argument('_id', type=str, required=True, location=['json'])
        args = parser.parse_args()

        _id = args['_id']

        msg = mongo_db['radiks-server-data'].find_one({'_id': _id, 'radiksType': 'msg'})

        if msg is None:
            abort(400)

        payload = msg['payload']
        name = payload['name']
        uid = payload['uid']

        if not is_domain_exists(name):
            rv = {
                'error': 1,
                'code': 10,
                'msg': 'Domain name does not exist'
            }
            return rv, 200

        session: Session = session_maker()
        rec: Domain = session.query(Domain).filter(Domain.name == name).first()

        if rec is not None and rec.uid != uid:
            session.close()
            rv = {
                'error': 1,
                'code': 12,
                'msg': 'Domain name already in use by another user'
            }
            return rv, 200

        if rec is None:
            rec = Domain(name, uid)
            session.add(rec)

        txt_records = get_txt_records(name)

        # Verified!
        if rec.txt in txt_records:
            rec.verified = 1
            rec.verification_date = now_utc()

        session.commit()
        rv = {
            'error': 0,
            'verified': rec.verified,
            'uid': rec.uid,
            'txt': rec.txt
        }
        session.close()

        return rv, 200
