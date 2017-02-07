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

-# create tables
-python manage.py migrate --noinput
-
-# copy static files
-python manage.py collectstatic --noinput

# load fixtures (order is important)
python manage.py loaddata /vagrant/fixtures/sites.json
python manage.py loaddata /vagrant/fixtures/users.json
python manage.py loaddata /vagrant/fixtures/appointments.json
python manage.py loaddata /vagrant/fixtures/folio.json
python manage.py loaddata /vagrant/fixtures/blog.json
python manage.py loaddata /vagrant/fixtures/eatshop.json
python manage.py loaddata /vagrant/fixtures/sagelist.json
python manage.py loaddata /vagrant/fixtures/mhdata.json

# load housing data
python manage.py load_dorms
python manage.py load_maps
python manage.py load_dorm_rooms
python manage.py loaddata /vagrant/fixtures/housing.json

# generate fake data for certain apps
python manage.py fakeevents
python manage.py scrape_twitter
python manage.py load_menus