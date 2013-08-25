#!/bin/bash
set -e
PIDFILE="/home/vagrant/run/gunicorn.pid"
SOCKFILE="/home/vagrant/run/gunicorn.sock"
RUN_GUNICORN_CMD="source /home/vagrant/env/bin/activate; /vagrant/manage.py run_gunicorn -c /vagrant/vagrant/gunicorn.cfg.py && echo Started!"

case "$1" in
    start)
        echo -n "Starting gunicorn... "
        if [ -f $PIDFILE ]; then
            echo "Already started!"
        else
            rm -f -- $SOCKFILE
            bash -c '$RUN_GUNICORN_CMD'
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
            bash -c '$RUN_GUNICORN_CMD'
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
