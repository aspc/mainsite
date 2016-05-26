import multiprocessing

RUN_DIR = "/home/vagrant/run"
bind = "unix:{0}/gunicorn.sock".format(RUN_DIR)
pidfile = "{0}/gunicorn.pid".format(RUN_DIR)
workers = 1
# good as poor-man's autoreload; force workers to exit after 1 request:
max_requests = 1
