from fabric.api import *

try:
    from config import host_strings # varies per-user, so not tracked in Git
    env.hosts = host_strings
except ImportError:
    env.hosts = ["peninsula.pomona.edu"]

env.site = env.branch = "staging" # By default, run all of these tasks on 'staging'

env.origin = "git@github.com:aspc/mainsite.git"

"""
Deployment script for ASPC's main site and staging site

Provides 'stage' as an alias for 'on_staging apply_changes'
and 'deploy' for 'on_main apply_changes'
"""

def on_staging():
    env.site = "staging"
    env.branch = "staging"

def on_main():
    env.site = "main"
    env.branch = "production"

def stage():
    on_staging()
    apply_changes()

def deploy():
    on_main()
    apply_changes()

def migrate():
    with settings(
        cd("/srv/www/{0}/mainsite".format(env.site)),
        prefix("source /srv/www/{0}/env/bin/activate".format(env.site))
    ):
        sudo("./manage.py migrate", user=env.site)
        sudo("./manage.py syncdb", user=env.site)

def update_static():
    with settings(
        cd("/srv/www/{0}/mainsite".format(env.site)),
        prefix("source /srv/www/{0}/env/bin/activate".format(env.site))
    ):
        sudo("./manage.py collectstatic", user=env.site)

def install_requirements():
    with settings(
        cd("/srv/www/{0}/mainsite".format(env.site)),
        prefix("source /srv/www/{0}/env/bin/activate".format(env.site))
    ):
        sudo("pip install -r ./requirements.txt", user=env.site)

def reload():
    run("/srv/www/{0}/bin/gunicorn.sh reload".format(env.site))

def git_push_pull():
    local("git push {0} master".format(env.origin))
    local("git checkout {0}".format(env.branch))
    local("git merge master")
    local("git push {0} {1}".format(env.origin, env.branch))
    local("git checkout master")
    local("git status")
    with settings(
        cd("/srv/www/{0}/mainsite".format(env.site)),
    ):
        sudo("git clean -f", user=env.site)
        sudo("git checkout -f .", user=env.site)
        sudo("git pull origin", user=env.site)
        sudo("git status", user=env.site)

def apply_changes():
    git_push_pull()
    install_requirements()
    update_static()
    migrate()
    reload()
