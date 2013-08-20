#!/usr/bin/env bash
export DEBIAN_FRONTEND=noninteractive
apt-get -y update

# Dependencies for ASPC Main Site
apt-get -y install build-essential git nginx postgresql libpq-dev python-dev python-virtualenv python-pip libldap2-dev libsasl2-dev libssl-dev python-psycopg2 curl unixodbc unixodbc-dev tdsodbc freetds-bin

# Set up PostgreSQL
cat /vagrant/vagrant/pg_hba_prepend.conf /etc/postgresql/9.1/main/pg_hba.conf > /tmp/pg_hba.conf
mv /tmp/pg_hba.conf /etc/postgresql/9.1/main/pg_hba.conf
sudo -u postgres psql -f /vagrant/vagrant/setup_postgres.sql
if [ $(sudo -u postgres psql -l | grep main_django | wc -l) -eq 0 ]; then
    echo -n "Creating a 'main_django' database..."
    sudo -u postgres psql -c "CREATE DATABASE main_django WITH OWNER = main" && echo "Done!"
else
    echo "Database 'main_django' already exists"
fi

# Some steps should be performed as the regular vagrant user
sudo -u vagrant bash /vagrant/vagrant/init_as_user.sh

# Set up public-facing nginx
rm -f /etc/nginx/sites-enabled/default
cp /vagrant/vagrant/frontend_nginx.conf /etc/nginx/sites-enabled/
service nginx restart
