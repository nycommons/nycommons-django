import contextlib

from fabric.api import *


env.hosts = ['nycommons_nycommons',]
env.use_ssh_config = True


server_project_dirs = {
    'dev': '/webapps/nycommons_dev/nycommons-django/',
    'prod': '/webapps/nycommons/nycommons-django/',
}

server_virtualenvs = {
    'dev': 'nycommons_dev',
    'prod': 'nycommons',
}

supervisord_programs = {
    'dev': 'django_dev',
    'prod': 'django',
}

supervisord_conf = '/etc/supervisor/supervisord.conf'


@contextlib.contextmanager
def cdversion(version, subdir=''):
    """cd to the version indicated"""
    with prefix('cd %s' % '/'.join([server_project_dirs[version], subdir])):
        yield


@contextlib.contextmanager
def workon(version):
    """workon the version of indicated"""
    with prefix('workon %s' % server_virtualenvs[version]):
        yield

@task
def pull(version='prod'):
    with cdversion(version):
        run('git pull')


@task
def install_requirements(version='prod'):
    with workon(version):
        with cdversion(version):
            run('pip install -r requirements/base.txt')
            run('pip install -r requirements/production.txt')


@task
def collect_static(version='prod'):
    with workon(version):
        run('django-admin collectstatic --noinput')


@task
def migrate(version='prod'):
    with workon(version):
        run('django-admin migrate')


@task
def restart_django(version='prod'):
    run('supervisorctl -c %s restart %s' % (
        supervisord_conf,
        supervisord_programs[version],
    ))


@task
def status():
    run('supervisorctl -c %s status' % supervisord_conf)


@task
def start(version='prod'):
    pull(version=version)
    install_requirements(version=version)
    migrate(version=version)
    collect_static(version=version)
    with workon(version):
        run('supervisorctl -c %s start %s' % (supervisord_conf,
                                              supervisord_programs[version]))


@task
def stop(version='prod'):
    with workon(version):
        run('supervisorctl -c %s stop %s' % (supervisord_conf,
                                             supervisord_programs[version]))


@task
def deploy_dev():
    pull(version='dev')
    install_requirements(version='dev')
    migrate(version='dev')
    collect_static(version='dev')
    restart_django(version='dev')


@task
def deploy():
    pull()
    install_requirements()
    migrate()
    collect_static()
    restart_django()
