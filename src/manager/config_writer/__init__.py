import os
from typing import List

from manager.db import session_maker
from manager.db_helper import get_config_checksum, set_config_checksum
from manager.helper import reload_nginx
from manager.logger import create_logger
from manager.model import Domain
from manager.util import md5_checksum

logger = create_logger('config-writer')


def gen_server_block(domain):
    temp = """server {
    listen 443 ssl;
    server_name <-domain->;
            
    location / {
        proxy_pass          http://up;
        proxy_redirect      off;
        proxy_set_header    Host $host;
        proxy_set_header    X-Real-IP $remote_addr;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Forwarded-Host $server_name;
    }
    
    ssl_certificate         /etc/letsencrypt/live/<-domain->/fullchain.pem;
    ssl_certificate_key     /etc/letsencrypt/live/<-domain->/privkey.pem;
    include                 /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam             /etc/letsencrypt/ssl-dhparams.pem;
}"""

    return temp.replace('<-domain->', domain)


def prepare_config(domains: List[str]) -> str:
    s = ''

    for d in domains:
        s = "{}\n{}".format(s, gen_server_block(d))

    return s


def writer(force=False):
    session = session_maker()

    domains: List[Domain] = session.query(Domain) \
        .filter(Domain.cert == 1) \
        .order_by(Domain.created.asc()).all()

    domain_names = [x.name for x in domains]

    config = prepare_config(domain_names)

    checksum = md5_checksum(config)

    if not force and checksum == get_config_checksum(session):
        session.close()
        return

    config_path = os.environ.get('CONF_FILE_PATH')
    with open(config_path, 'w') as f:
        f.write(config)
        f.close()

    set_config_checksum(session, checksum)

    logger.info('New config has written to {}'.format(config_path))

    session.commit()
    session.close()

    reload_nginx()

    logger.info('Nginx reloaded')
