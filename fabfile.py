import os
from contextlib import contextmanager
from fabric.api import cd, env, prefix, run, sudo, task
from fabric.context_managers import settings, shell_env
from fabric.contrib.files import exists, upload_template

PROJECT_NAME = 'sci_blog'
PROJECT_ROOT = '/var/www/%s' % PROJECT_NAME
VENV_DIR = os.path.join(PROJECT_ROOT, 'myvenv')
REPO = 'https://github.com/Ranc58/37_transcendence_1.git'
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_URI = "postgres://{USER}:{PASSWORD}@localhost:5432/{USER}".format(
    USER=PROJECT_NAME,
    PASSWORD=DB_PASSWORD,
)
CONFIG = os.getenv('DJANGO_CONFIGURATION')

env.hosts = [os.getenv('SSH_HOST')]
env.forward_agent = True


@contextmanager
def source_virtualenv():
    with prefix('source ' + os.path.join(VENV_DIR, 'bin/activate')):
        yield


def chown():
    sudo('chown -R www-data:www-data %s' % PROJECT_ROOT)


def restart():
    sudo('service nginx restart')


def create_database():
    run('sudo -i -u postgres psql -c '
        '"CREATE USER {PROJECT_NAME} WITH PASSWORD \'{PASSWORD}\';"'.format(
            PROJECT_NAME=PROJECT_NAME,
            PASSWORD=DB_PASSWORD
        ))
    run('sudo -i -u postgres psql -c '
        '"CREATE DATABASE {PROJECT_NAME} WITH OWNER {PROJECT_NAME};"'.format(
            PROJECT_NAME=PROJECT_NAME
        ))


def update_project():
    with cd(PROJECT_ROOT):
        run('git pull origin master')
        run('python3 -m venv myvenv')
        with source_virtualenv():
            with prefix(
                    'export DJANGO_SETTINGS_MODULE={settings}.settings '
                    '&& export DJANGO_CONFIGURATION={conf}'.format(
                        settings=PROJECT_NAME,
                        conf=CONFIG
                    )), shell_env(DB_URI=DB_URI):
                run('source myvenv/bin/activate')
                run('pip3 install -r requirements.txt')
                run('python3 manage.py collectstatic --noinput')
                run('python3 manage.py migrate')


def clone_project():
    run('mkdir -p project_name')
    sudo('mkdir -p {}'.format(PROJECT_ROOT))
    sudo('chown -R {}:{} {}'.format(env.user, env.user, PROJECT_ROOT))
    run('git clone {} {}'.format(REPO, PROJECT_ROOT))


def update_server():
    sudo(
        'apt-get update && apt-get install '
        'git nginx libjpeg8-dev postgresql'
        ' libpq-dev python3-dev python3-pip '
        'python3-venv libfreetype6-dev '
        'libncurses5-dev'
    )


def configure_nginx():
    conf_filepath = '/etc/nginx/sites-available/{PROJECT_NAME}.conf'.format(
        PROJECT_NAME=PROJECT_NAME
    )
    context = {
        'PROJECT_NAME': PROJECT_NAME,
        'HOST': '85.143.223.88'
    }
    upload_template(
        'nginx.conf',
        conf_filepath,
        context=context,
        template_dir='conf_templates',
        use_jinja=True,
    )
    if not exists(conf_filepath):
        sudo('ln -s /etc/nginx/sites-available/{project_name}.conf '
             '/etc/nginx/sites-enabled/'.format(
                project_name=PROJECT_NAME))


def configure_systemd():
    systemd_filepath = '/etc/systemd/system/{PROJECT_NAME}.service'.format(
        PROJECT_NAME=PROJECT_NAME
    )
    context = {
        'DB_URI': DB_URI,
        'SECRET_KEY_DJANGO': os.getenv('SECRET_KEY_DJANGO'),
        'SENTRY_DSN': os.getenv('SENTRY_DSN'),
        'VENV_DIR': VENV_DIR,
        'PROJECT_ROOT': PROJECT_ROOT,
    }
    upload_template(
        'sci_blog.service',
        systemd_filepath,
        context=context,
        template_dir='conf_templates',
        use_jinja=True,
    )
    run('systemctl enable {PROJECT_NAME}.service'.format(
        PROJECT_NAME=PROJECT_NAME
    ))


@task
def bootstrap():
    update_server()
    if not exists(PROJECT_ROOT):
        clone_project()
        create_database()
    configure_nginx()
    restart()
    chown()
    update_project()
    configure_systemd()
    run('sudo service sci_blog restart')


@task
def drop_db():
    stop_service()
    run('sudo -i -u postgres psql -c "DROP DATABASE {PROJECT_NAME};"'.format(
        PROJECT_NAME=PROJECT_NAME
    ))
    run('sudo -i -u postgres psql -c "DROP USER {PROJECT_NAME};"'.format(
        PROJECT_NAME=PROJECT_NAME,
    ))


@task
def restart_service():
    run('sudo service sci_blog restart')


@task
def stop_service():
    run('sudo service sci_blog stop')


@task
def status_service():
    run('sudo service sci_blog status')


@task
def create_superuser():
    with cd(PROJECT_ROOT), source_virtualenv():
        with prefix('export DJANGO_SETTINGS_MODULE={}.settings'.format(
                PROJECT_NAME)), shell_env(DB_URI=DB_URI), settings(prompts={
                "Password: ": os.getenv('ADMIN_PASS'),
                "Password (again): ": os.getenv('ADMIN_PASS'),
                }):
                    run('python3 manage.py createsuperuser'
                        ' --username admin'
                        ' --email admin@example.com')
