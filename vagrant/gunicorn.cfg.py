import multiprocessing

RUN_DIR = "/home/vagrant/run"
bind = "unix:{0}/gunicorn.sock".format(RUN_DIR)
pidfile = "{0}/gunicorn.pid".format(RUN_DIR)
workers = multiprocessing.cpu_count() * 2 + 1
daemon = True
