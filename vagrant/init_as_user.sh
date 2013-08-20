#!/usr/bin/env bash
echo "ulimit -n 2048" >> /home/vagrant/.profile
cd /home/vagrant

# create dirs expected by nginx config
mkdir -p run public logs config

# set up python virtualenv
virtualenv /home/vagrant/env
source /home/vagrant/env/bin/activate
pip install -r /vagrant/requirements.txt

# create settings if they do not exist
if [ ! -f /vagrant/aspc/settings.py ];
then
    echo "Creating development settings.py from settings.py.example..."
    cp /vagrant/aspc/settings.py.example /vagrant/aspc/settings.py
fi

# create tables / set up ASPC mainsite
/vagrant/manage.py syncdb --noinput
/vagrant/manage.py migrate --noinput
/vagrant/manage.py collectstatic --noinput
/vagrant/manage.py loaddata /vagrant/fixtures/*

# start gunicorn
/vagrant/vagrant/gunicorn.sh start

# start backend nginx
mkdir -p /home/vagrant/temp/nginx/proxy /home/vagrant/temp/nginx/fastcgi /home/vagrant/temp/nginx/uwsgi /home/vagrant/temp/nginx/scgi
cp /vagrant/vagrant/backend_nginx.conf /home/vagrant/config/nginx.conf
/vagrant/vagrant/httpd.sh start
