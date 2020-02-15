import tldextract
from flask_restful import reqparse, Resource


class DomainExtractResource(Resource):

    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        parser.add_argument('name', type=str, required=True, location=['args', 'json'])
        args = parser.parse_args()

        name = args['name']

        ext = tldextract.extract(name)

        return {'domain': '{}.{}'.format(ext.domain, ext.suffix), 'subDomain': ext.subdomain}, 200
