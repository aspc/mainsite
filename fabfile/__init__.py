from fabric.api import *

try:
    from config import host_strings # varies per-user, so not tracked in Git
    env.hosts = host_strings
except ImportError:
    env.hosts = ["peninsula.pomona.edu"]

env.site = "staging" # By default, run all of these tasks on 'staging'

"""
Deployment script for ASPC's main site and staging site

Provides 'stage' as an alias for 'on_staging apply_changes'
and 'deploy' for 'on_main apply_changes'
"""

def on_staging():
    env.site = "staging"

def on_main():
    env.site = "main"

def stage():
    on_staging()
    apply_changes()

def deploy():
    on_main()
    apply_changes()

def migrate():
    with settings(
        cd("/srv/www/{0}/env/aspcrepo/aspc".format(env.site)),
        prefix("source /srv/www/{0}/env/bin/activate".format(env.site))
    ):
        run("./manage.py migrate")
        run("./manage.py syncdb")

def update_static():
    with settings(
        cd("/srv/www/{0}/env/aspcrepo/aspc".format(env.site)),
        prefix("source /srv/www/{0}/env/bin/activate".format(env.site))
    ):
        run("./manage.py collectstatic")

def reload():
    run("/srv/www/{0}/bin/gunicorn.sh reload".format(env.site))

def apply_changes():
    local("git push {0}".format(env.site))
    with cd("/srv/www/{0}/env/aspcrepo".format(env.site)):
        run("git pull")
        run("git merge origin/master")
        run("git status")
    
    migrate()
    update_static()
    reload()
