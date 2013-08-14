#!/usr/bin/env bash
echo "ulimit -n 2048" >> ~/.profile
cd /home/vagrant
mkdir -p run public logs config
virtualenv /home/vagrant/env
source /home/vagrant/env/bin/activate
pip install -r /vagrant/requirements.txt
/vagrant/vagrant/gunicorn.sh start
mkdir -p /home/vagrant/temp/nginx/proxy /home/vagrant/temp/nginx/fastcgi /home/vagrant/temp/nginx/uwsgi /home/vagrant/temp/nginx/scgi
cp /vagrant/vagrant/backend_nginx.conf /home/vagrant/config/nginx.conf
/vagrant/vagrant/httpd.sh start
