from flask import Flask
from flask_restful import Api
from werkzeug.middleware.proxy_fix import ProxyFix

from manager.api.resources import (IndexResource,
                                   HostIpResource,
                                   DomainVerificationResource,
                                   DomainExtractResource,
                                   ProjectResource)

app = None


def __flask_setup():
    global app

    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    api = Api(app)

    api.add_resource(IndexResource, '/')
    api.add_resource(HostIpResource, '/host-ip')
    api.add_resource(DomainVerificationResource, '/domain-verification')
    api.add_resource(DomainExtractResource, '/domain-extract')
    api.add_resource(ProjectResource, '/project')


def __run_dev_server():
    global app

    from flask_cors import CORS
    CORS(app)

    app.config['DEVELOPMENT'] = True
    app.config['DEBUG'] = True

    app.run(host='127.0.0.1', port=8088)


__flask_setup()


def main():
    __run_dev_server()
