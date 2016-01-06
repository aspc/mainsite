# Deployment script for ASPC's main site and staging site

from fabric.api import *

try:
	from config import host_strings # Varies per-user, so not tracked in Git
	env.hosts = host_strings
except ImportError:
	env.hosts = ['peninsula.pomona.edu']

env.site = env.branch = 'staging'
env.origin = 'git@github.com:aspc/mainsite.git'

## Fab methods

# Deploys `master` to the ASPC mainsite
# e.g. `fab deploy`
def deploy():
	env.site = 'main'
	env.branch = 'production'

	# Merges `master` into `production`
	_git_merge()

	# Pushes `production` to the origin
	_git_push()

	# Pulls `production` down onto the ASPC mainsite
	_git_pull()

	# Reloads the server, etc.
	_apply_changes()

# Deploys a given branch to the ASPC staging environment
# e.g. `fab stage:master`
def stage(branch):
	env.site = 'staging'
	env.branch = branch

	# Pushes the given branch to the origin
	_git_push()

	# Pulls the given branch down onto the ASPC staging site
	_git_pull()

	# Reloads the server, etc.
	_apply_changes()


## Helper methods

# Applies the changes contained in the newly-pulled branch
def _apply_changes():
	_install_requirements()
	_update_static()
	_migrate()
	_reload()

# Performs any new database migrations
def _migrate():
	with settings(
		cd('/srv/www/{0}/mainsite'.format(env.site)),
		prefix('source /srv/www/{0}/env/bin/activate'.format(env.site))
	):
		sudo('./manage.py migrate', user=env.site)

# Refreshes the static assets that are served
def _update_static():
	with settings(
		cd('/srv/www/{0}/mainsite'.format(env.site)),
		prefix('source /srv/www/{0}/env/bin/activate'.format(env.site))
	):
		sudo('./manage.py collectstatic', user=env.site)
		# TODO: Reenable this once Django Compressor supports offline compression for Django 1.9
		#sudo('./manage.py compress', user=env.site)

# Installs any new Python requirements in requirements.txt
def _install_requirements():
	with settings(
		cd('/srv/www/{0}/mainsite'.format(env.site)),
		prefix('source /srv/www/{0}/env/bin/activate'.format(env.site))
	):
		sudo('pip install -r ./requirements.txt', user=env.site)

# Reloads GUnicorn to serve the latest files
def _reload():
	run('/srv/www/{0}/bin/gunicorn.sh reload'.format(env.site))

# Pushes the given branch to the origin
def _git_push():
	local('git push {0} {1}'.format(env.origin, env.branch))

# Merges `master` into `production`
def _git_merge():
	# Sync `master` with the origin, hopefully all merge conflicts should have already been resolved...
	local('git checkout master')
	local('git pull')
	local('git push {0} master'.format(env.origin))

	# Merge `production` into `master`
	local('git checkout {0}'.format(env.branch))
	local('git pull')
	local('git merge master --no-ff')

	# Clean up
	local('git checkout master')
	local('git status')

# Pulls down the given branch to Peninsula
def _git_pull():
	with settings(
		cd('/srv/www/{0}/mainsite'.format(env.site)),
	):
		# Check for accidental overwrite of changes made on Peninsula that haven't been committed
		sudo('git status')
		sudo('git clean -dfn --exclude="log/"', user=env.site)
		prompt('Overwrite untracked files on {0}? Type "yes" to continue, or "no" to cancel:'.format(env.site), key='should_overwrite')
		if env.should_overwrite != 'yes':
			abort()

		# Reset the working directory on Peninsula to a clean state
		sudo('git clean -df --exclude="log/"', user=env.site)
		sudo('git reset --hard HEAD', user=env.site)

		# Pull down the new branch
		sudo('git fetch --all', user=env.site)
		sudo('git checkout {0}'.format(env.branch), user=env.site)
		sudo('git reset --hard origin/{0}'.format(env.branch), user=env.site)
		sudo('git status', user=env.site)
