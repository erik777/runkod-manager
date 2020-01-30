import os
from shutil import copyfile
from subprocess import run, PIPE

from manager.model import Project


def create_cert(project: Project) -> bool:
    # Create cert
    cmd = ['certbot', 'certonly', '--webroot', '-w', os.environ.get('CERT_WEB_ROOT'), '--email',
           os.environ.get('CERT_EMAIL'), '--agree-tos', '--force-renewal',
           '--preferred-challenges', 'http', '-d', project.name]
    out = run(cmd, stdout=PIPE, stderr=PIPE)

    if out.returncode != 0:
        return False

    # Copy cert files
    le_cert_dir = os.environ.get('LE_CERT_BASE_DIR')
    cert_dir = os.environ.get('CERT_BASE_DIR')

    cert_path = os.path.join(le_cert_dir, project.name, 'fullchain.pem')
    new_cert_path = os.path.join(cert_dir, '{}.pem'.format(project.name))

    cert_key_path = os.path.join(le_cert_dir, project.name, 'privkey.pem')
    new_cert_key_path = os.path.join(cert_dir, '{}.key.pem'.format(project.name))

    copyfile(cert_path, new_cert_path)
    copyfile(cert_key_path, new_cert_key_path)

    # Delete cert records from certbot
    cmd = ['certbot', 'delete', '--cert-name', project.name]
    out = run(cmd, stdout=PIPE, stderr=PIPE)
    if out.returncode != 0:
        return False

    # Add cert file binaries to db entity
    with open(new_cert_path, 'rb') as f:
        project.cert_file = f.read()
        f.close()

    with open(new_cert_key_path, 'rb') as f:
        project.cert_key_file = f.read()
        f.close()

    return True


def reload_nginx():
    cmd = ['nginx', '-s', 'reload']
    out = run(cmd, stdout=PIPE, stderr=PIPE)
    return out.returncode == 0
