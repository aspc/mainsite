#!/usr/bin/env bash
set -e

function info {
    echo "$(tput bold)$(tput setaf 3)[*****] $1$(tput sgr0)"
}

function err {
    echo "$(tput bold)$(tput setaf 1)[!!!!!] $1$(tput sgr0)"
}

export DEBIAN_FRONTEND=noninteractive
update-locale LANG=en_US.UTF-8
if [ -f /root/apt.updated ]; then
    filemtime=`stat -c %Y /root/apt.updated`
    currtime=`date +%s`
    diff=$(( (currtime - filemtime) / 86400 ))
    if [ $diff -gt 7 ]; then
        info "Last update more than a week ago, running apt-get update"
        apt-get -y update
        touch /root/apt.updated
    else
        info "Recently ran apt-get update ($diff days ago), skipping"
    fi
else
    info "First boot, running apt-get update"
    apt-get -y update
    touch /root/apt.updated
fi


# Dependencies for ASPC Main Site
apt-get -y install build-essential git nginx postgresql libpq-dev python-dev \
    python-virtualenv python-pip libsasl2-dev libssl-dev libffi-dev \
    python-psycopg2 curl libjpeg-dev libxml2-dev libxslt-dev

# Set up PostgreSQL
/etc/init.d/postgresql stop
cat /vagrant/vagrant/db/pg_hba_prepend.conf /etc/postgresql/9.3/main/pg_hba.conf > /tmp/pg_hba.conf
mv /tmp/pg_hba.conf /etc/postgresql/9.3/main/pg_hba.conf
/etc/init.d/postgresql start
info "Waiting for PostgreSQL to finish starting"
sleep 5

info "Creating user 'main' in PostgreSQL (if it doesn't exist)"
sudo -u postgres psql -f /vagrant/vagrant/db/setup_postgres.sql

if [ $(sudo -u postgres psql -l | grep main_django | wc -l) -eq 0 ]; then
    info "Creating a 'main_django' database..."
    # Can't get Ubuntu 12.04 to install Postgres with a sensible default locale
    # so we a) create the db from template0 and b) specify en_US.utf8
    sudo -u postgres psql -c "CREATE DATABASE main_django WITH ENCODING = 'UTF-8' LC_CTYPE = 'en_US.UTF-8' LC_COLLATE = 'en_US.UTF-8' OWNER main TEMPLATE template0" && info "Done!"
else
    info "Database 'main_django' already exists"
fi

# Some steps should be performed as the regular vagrant user
sudo -u vagrant bash /vagrant/vagrant/init/init_as_user.sh

# Set up public-facing nginx
rm -f /etc/nginx/sites-enabled/default
cp /vagrant/vagrant/srv/frontend_nginx.conf /etc/nginx/sites-enabled/
service nginx restart && info "Started nginx"

# Start GUnicorn as a daemon process
cd /vagrant && /home/vagrant/env/bin/gunicorn -c /vagrant/vagrant/srv/gunicorn.cfg.py aspc.wsgi:application -D && info "Started GUnicorn"