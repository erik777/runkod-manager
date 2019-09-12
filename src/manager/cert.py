import os
from subprocess import run, PIPE


def create_cert(domain: str) -> bool:
    cmd = ['certbot', 'certonly', '--webroot', '-w', os.environ.get('CERT_WEB_ROOT'), '--email',
           os.environ.get('CERT_EMAIL'), '--agree-tos', '--preferred-challenges', 'http', '-d', domain]
    out = run(cmd, stdout=PIPE, stderr=PIPE)
    return out.returncode == 0


def delete_cert(domain: str) -> bool:
    cmd = ['certbot', 'delete', '--cert-name', domain]
    out = run(cmd, stdout=PIPE, stderr=PIPE)
    return out.returncode == 0
