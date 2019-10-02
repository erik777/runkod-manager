import os
from typing import List

from manager.db import session_maker
from manager.db_helper import get_config_checksum, set_config_checksum
from manager.helper import reload_nginx
from manager.logger import create_logger
from manager.model import Domain
from manager.util import md5_checksum, assert_env_vars

assert_env_vars('CONF_DIR', 'CONF_FILE', 'CERT_BASE_DIR')

logger = create_logger('config-writer')


def gen_server_block(domain: Domain) -> str:
    temp = """server {
    listen 443 ssl;
    listen 80;

    server_name <-domain->;

    location / {
        proxy_pass  http://up;
        include     <-config_dir->/proxy_params;
    }

    ssl_certificate         <-cert_base_dir->/<-domain->.pem;
    ssl_certificate_key     <-cert_base_dir->/<-domain->.key.pem;
    include                 /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam             /etc/letsencrypt/ssl-dhparams.pem;
}"""

    return temp.replace('<-domain->', domain.name) \
        .replace('<-config_dir->', os.environ.get('CONF_DIR')) \
        .replace('<-cert_base_dir->', os.environ.get('CERT_BASE_DIR'))


def prepare_config(domains: List[Domain]) -> str:
    s = ''

    for d in domains:
        s = "{}\n{}".format(s, gen_server_block(d))

    return s


def writer(force=False):
    session = session_maker()

    domains: List[Domain] = session.query(Domain) \
        .filter(Domain.cert_status == 1) \
        .order_by(Domain.created.asc()).all()

    config = prepare_config(domains)

    checksum = md5_checksum(config)

    curr_checksum = get_config_checksum(session)
    if not force and checksum == curr_checksum:
        session.close()
        return

    config_path = os.path.join(os.environ.get('CONF_DIR'), os.environ.get('CONF_FILE'))

    with open(config_path, 'w') as f:
        f.write(config)
        f.close()

    set_config_checksum(session, checksum)

    logger.info('New config has written to {}'.format(config_path))

    session.commit()
    session.close()

    reload_nginx()

    logger.info('Nginx reloaded')
