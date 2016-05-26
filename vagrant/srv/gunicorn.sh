#!/bin/bash
set -e
PIDFILE="/home/vagrant/run/gunicorn.pid"
SOCKFILE="/home/vagrant/run/gunicorn.sock"
RUN_GUNICORN_CMD="/home/vagrant/env/bin/gunicorn -c /vagrant/vagrant/srv/gunicorn.cfg.py aspc.wsgi:application -D"

case "$1" in
    start)
        echo -n "Starting gunicorn... "
        if [ -f $PIDFILE ]; then
            echo "Already started!"
        else
            rm -f -- $SOCKFILE
            pushd /vagrant
            $RUN_GUNICORN_CMD
            popd
            echo "Started!"
        fi
        ;;
    stop)
        echo -n "Stopping gunicorn... "
        if [ -f $PIDFILE ]; then
            kill `cat -- $PIDFILE`
            rm -f -- $PIDFILE
            rm -f -- $SOCKFILE
            echo "Stopped!"
        else
            echo "No gunicorn running, or missing PID file!"
        fi
        ;;
    reload)
        echo -n "Reloading... "
        if [ -f $PIDFILE ]; then
            kill -HUP `cat $PIDFILE`
            echo "Reloaded!"
        else
            echo "No gunicorn running, starting..."
            rm -f -- $SOCKFILE
            pushd /vagrant
            $RUN_GUNICORN_CMD
            popd
            echo "Started!"
        fi
        ;;
    status)
        if [ ! -f $PIDFILE ]; then
            echo "stopped"
        elif [ $(ps x | grep gunicorn | grep `cat -- $PIDFILE` | wc -l) -ne 0 ]; then
            echo "running"
        else
            echo "missing (pidfile exists, but there is no process with this pid)"
            echo "removing stale pidfile"
            rm -f -- $PIDFILE
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|reload|status}"
        exit 1
        ;;
esac
