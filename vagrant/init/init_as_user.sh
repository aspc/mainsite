#!/usr/bin/env bash
cd /home/vagrant

# Up the ulimit (intended for watchmedo, may not be necessary)
if grep -Fxq "ulimit -n 2048" /home/vagrant/.profile
then
    echo "Already have ulimit line in ~/.profile"
else
    echo "Upping ulimit to 2048 in ~/.profile"
    echo "ulimit -n 2048" >> /home/vagrant/.profile
    ulimit -n 2048
fi

# pre-populate ssh known_hosts with the Peninsula pubkey
mkdir -p /home/vagrant/.ssh
if [ ! -f /home/vagrant/.ssh/known_hosts ]; then
    cp /vagrant/vagrant/init/known_hosts /home/vagrant/.ssh/known_hosts
fi

# set up python virtualenv if it doesn't exist
if [ ! -f /home/vagrant/env/bin/activate ];
then
    virtualenv /home/vagrant/env
fi

# Create folder for GUnicorn socket and pidfile
mkdir -p /home/vagrant/run

# Activate virtualenv on login
if grep -Fxq "source /home/vagrant/env/bin/activate" /home/vagrant/.profile
then
    echo "Already have virtualenv activate line in ~/.profile"
else
    echo "Adding line to ~/.profile to activate virtualenv on login"
    echo "source /home/vagrant/env/bin/activate" >> /home/vagrant/.profile
fi

source /home/vagrant/env/bin/activate
pip install -r /vagrant/requirements.txt

# create settings if they do not exist
if [ ! -f /vagrant/aspc/settings.py ];
then
    echo "Creating development settings.py from settings.py.example..."
    cp /vagrant/aspc/settings.py.example /vagrant/aspc/settings.py
fi

# create tables
/vagrant/manage.py migrate --noinput

# copy static files
/vagrant/manage.py collectstatic --noinput

# load fixtures (order is important)
/vagrant/manage.py loaddata /vagrant/fixtures/sites.json
/vagrant/manage.py loaddata /vagrant/fixtures/users.json
/vagrant/manage.py loaddata /vagrant/fixtures/appointments.json
/vagrant/manage.py loaddata /vagrant/fixtures/folio.json
/vagrant/manage.py loaddata /vagrant/fixtures/blog.json
/vagrant/manage.py loaddata /vagrant/fixtures/eatshop.json
/vagrant/manage.py loaddata /vagrant/fixtures/sagelist.json

# load housing data
/vagrant/manage.py load_dorms
/vagrant/manage.py load_maps
/vagrant/manage.py load_dorm_rooms
/vagrant/manage.py loaddata /vagrant/fixtures/housing.json

# generate fake data for certain apps
/vagrant/manage.py fakeevents
/vagrant/manage.py scrape_twitter
/vagrant/manage.py load_menus