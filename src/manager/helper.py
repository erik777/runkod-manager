import os
import socket
from subprocess import run, PIPE


def domain_ip(domain: str) -> str:
    return socket.gethostbyname(domain)


def create_cert(domain: str) -> bool:
    cmd = ['certbot', 'certonly', '--webroot', '-w', os.environ.get('CERT_WEB_ROOT'), '--email',
           os.environ.get('CERT_EMAIL'), '--agree-tos', '--force-renewal',
           '--preferred-challenges', 'http', '-d', domain]
    out = run(cmd, stdout=PIPE, stderr=PIPE)

    if out.returncode == 0:
        return False

    return True


def delete_cert(domain: str) -> bool:
    cmd = ['certbot', 'delete', '--cert-name', domain]
    out = run(cmd, stdout=PIPE, stderr=PIPE)
    return out.returncode == 0


def reload_nginx():
    cmd = ['nginx', '-s', 'reload']
    out = run(cmd, stdout=PIPE, stderr=PIPE)
    return out.returncode == 0
