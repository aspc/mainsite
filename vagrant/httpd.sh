#!/bin/bash
set -e
ROOT="/home/vagrant"
PIDFILE="$ROOT/run/nginx.pid"

case "$1" in
    start)
        echo -n "Starting nginx... "
        if [ -f $PIDFILE ]; then
            if [ $(ps x | grep nginx | grep `cat -- $PIDFILE` | wc -l) -ne 0 ]; then
                echo "Already started!"
                exit 0
            fi
        fi
        rm -f -- $PIDFILE
        echo
        nginx -p $ROOT/ -c $ROOT/config/nginx.conf 
        echo "Started!"
        ;;
    stop)
        echo -n "Stopping nginx... "
        if [ -f $PIDFILE ]; then
            kill `cat -- $PIDFILE`
            rm -f -- $PIDFILE
            echo "Stopped!"
        else
            echo "No nginx running, or missing PID file!"
        fi
        ;;
    restart)
        echo "Restarting nginx..."
        /vagrant/vagrant/httpd.sh stop
        /vagrant/vagrant/httpd.sh start
        ;;
    reload)
        echo "Reloading nginx configuration..."
        kill -HUP `cat -- $PIDFILE`
        echo "Done!"
        ;;
    status)
        if [ ! -f $PIDFILE ]; then
            echo "stopped"
        elif [ $(ps x | grep nginx | grep `cat -- $PIDFILE` | wc -l) -ne 0 ]; then
            echo "running"
        else
            echo "missing (pidfile exists, but there is no process with this pid)"
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|reload|status}"
        exit 1
        ;;
esac