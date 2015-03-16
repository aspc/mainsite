# ASPC Main Site #

The ASPC main site is developed and maintained by the [ASPC Digital Media and Programming Group](https://aspc.pomona.edu/senate/digital-media-programming/), a subsidiary of ASPC's communications arm. The goal of the main site is to provide useful and reliable services, tools, and information to the ASPC constituency - namely the students of Pomona College.

The ASPC main site is deployed at [https://aspc.pomona.edu](https://aspc.pomona.edu).

## Contributing ##

The ASPC main site is an open-source project that welcomes contributions from the community. If you want to be paid for your work, you should apply for a job in the [ASPC Digital Media and Programming Group](https://aspc.pomona.edu/senate/digital-media-programming/)!

### Development ###

To start hacking on the ASPC main site, you will need [Vagrant](https://www.vagrantup.com), a tool that will allow you to create a VM running on your machine that resembles our production environment. Vagrant runs on Windows, OSX, and Linux.

You will also need to fork the ASPC repository and clone it to your computer. Once you have done that and you have Vagrant installed, navigate to the directory where you cloned the repo, and run:

```
    vagrant up
```

This starts the VM. To see it in action, visit [http://localhost:8080](http://localhost:8080). For development, log in with username `developer` and password `developer`.

To run management commands, you'll need to ssh in to the VM:

```
    $ vagrant ssh
    vagrant$ cd /vagrant
    vagrant$ ./manage.py shell_plus
```

When you're done working, free up system resources with a `vagrant halt`. If you want to start from scratch, `vagrant destroy` and then `vagrant up` anew. Applying future changes to the Vagrant setup will be done automatically when you `vagrant up`, but you can also run `vagrant provision` yourself.

GUnicorn workers have `max_requests = 1` set in `vagrant/gunicorn.cfg.py`. This means that after at most one refresh, the worker will be running your code. If you need to force a reload, use `vagrant ssh -c "service gunicorn reload"`.

### Pull requests ###
 
When you have finished making changes on whatever branch in your forked repo, simply open a pull request against ASPC's `master` to signal that you'd like to merge them in. One of the ASPC developers will review the request, merge, and deploy it if it is appropriate. Feel free to contact [digitalmedia@aspc.pomona.edu](mailto:digitalmedia@aspc.pomona.edu) with any questions!


## Project Layout ##

Under the main `aspc` folder in this directory are several subfolders, most of
which are Django "apps":

- `activityfeed` - Feed of activity on Twitter, SageBooks, etc. (shown on homepage)
- `auth` - Django auth backend for Pomona College accounts
- `blog` - The senate blog (shown on homepage)
- `courses` - Course search and schedule builder
- `coursesearch` - Legacy course search & schedule builder
- `eatshop` - Local business and discount directory
- `events` - 5C event calendar and scraper (shown on homepage)
- `folio` - Simple CMS to add pages to ASPC site
- `housing` - Housing directory and reviews
- `menu` - 5C weekly dining hall menus (shown on homepage)
- `minutes` - History of ASPC minutes and summaries
- `sagelist` - Aka SageBooks, student-to-student textbook sales
- `senate` - Positions, appointments, and documents. Includes functionality to apply appropriate permissions to Senators when they log in during or after their tenure as senators


Folders without an `__init__.py` are not apps, but contain supporting files:

- `fixtures` - Fixture data for Coop Fountain page
- `maps` - Residence hall maps for Housing app
- `static` - Static assets (CSS/JavaScript) used in the site
- `templates` - Certain site-wide templates that don't fit into a particular app

And some apps are placeholders that have yet to be fleshed out or removed:

- `college` - Unused
- `map` - Unused
- `stream` - Unused
- `vote` - Unused


## Running Locally ##

If you cannot use Vagrant for some reason, you can always get the main site running locally the old-fashioned way. To do this, you need Python >= 2.7 (<3.0), PostgreSQL, virtualenv, virtualenvwrapper, and some patience. These instructions assume you are using a Mac with [Homebrew](http://brew.sh/) installed.

```
    brew install unixodbc # needed to compile pyodbc
    brew install freetds # needed to connect to JICSWS
    brew intall postgresql # for running a server locally
    mkvirtualenv aspc
    cd /path/to/your/mainsite/repo
    pip install -r requirements.txt # this will take a while
    
    # to start the PostgreSQL server before starting work:
    postgres -D /usr/local/var/postgres
    # alternatively, set it to start at login...
    ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents
    # ...and launch it now
    launchctl load ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist
    
    # create the db
    createdb
    psql -c "CREATE ROLE main LOGIN PASSWORD 'dev_password';"
    psql -c "CREATE DATABASE main_django WITH ENCODING = 'UTF-8' LC_CTYPE = 'en_US.UTF-8' LC_COLLATE = 'en_US.UTF-8' OWNER main TEMPLATE template0"
    
    # create db tables and superuser
    ./manage.py syncdb
    ./manage.py migrate
    
    # load default data
    ./manage.py loaddata ./fixtures/*
    
    # load housing data
    ./manage.py load_dorms
    ./manage.py load_maps
    ./manage.py load_dorm_rooms
```