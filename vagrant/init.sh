#!/usr/bin/env bash
export DEBIAN_FRONTEND=noninteractive
apt-get -y update
apt-get -y install build-essential git nginx postgresql libpq-dev python-dev python-virtualenv python-pip libldap2-dev libsasl2-dev libssl-dev python-psycopg2 curl unixodbc unixodbc-dev tdsodbc freetds-bin
sudo -u vagrant bash /vagrant/vagrant/init_as_user.sh
cp /vagrant/vagrant/frontend_nginx.conf /etc/nginx/sites-enabled/
service nginx stop
rm /etc/nginx/sites-enabled/default
service nginx start
