#!/usr/bin/env bash
export DEBIAN_FRONTEND=noninteractive
update-locale LANG=en_US.UTF-8
apt-get -y update

# Dependencies for ASPC Main Site
apt-get -y install build-essential git nginx postgresql libpq-dev python-dev python-virtualenv python-pip libldap2-dev libsasl2-dev libssl-dev python-psycopg2 curl unixodbc unixodbc-dev tdsodbc freetds-bin

# Set up PostgreSQL
cat /vagrant/vagrant/pg_hba_prepend.conf /etc/postgresql/9.1/main/pg_hba.conf > /tmp/pg_hba.conf
mv /tmp/pg_hba.conf /etc/postgresql/9.1/main/pg_hba.conf
service postgresql restart
sudo -u postgres psql -f /vagrant/vagrant/setup_postgres.sql
if [ $(sudo -u postgres psql -l | grep main_django | wc -l) -eq 0 ]; then
    echo -n "Creating a 'main_django' database..."
    # Can't get Ubuntu 12.04 to install Postgres with a sensible default locale
    # so we a) create the db from template0 and b) specify en_US.utf8
    sudo -u postgres psql -c "CREATE DATABASE main_django WITH ENCODING = 'UTF-8' LC_CTYPE = 'en_US.UTF-8' LC_COLLATE = 'en_US.UTF-8' OWNER main TEMPLATE template0" && echo "Done!"
else
    echo "Database 'main_django' already exists"
fi

# Some steps should be performed as the regular vagrant user
sudo -u vagrant bash /vagrant/vagrant/init_as_user.sh

# Set up service to reload gunicorn on changes
cp /vagrant/vagrant/watcher.conf /etc/init/
start watcher

# Set up public-facing nginx
rm -f /etc/nginx/sites-enabled/default
cp /vagrant/vagrant/frontend_nginx.conf /etc/nginx/sites-enabled/
service nginx restart
