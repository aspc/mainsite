## FIXME: Removed for Django 1.8 upgrade
# from __future__ import absolute_import
# from celery import Celery
# import os
#
# set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aspc.settings')
# from django.conf import settings
#
# app = Celery('aspc')
#
# Using a string here means the worker will not have to
# pickle the object when using Windows.
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#
# import os.path
# import time
#
# @app.task
# def save_timestamp():
#     """
#     Saves a timestamp to PROJECT_ROOT/celery_test.tmp
#
#     Useful for testing if the workers and result backend are
#     running (also returns the timestamp as a string in the result).
#     """
#     now = time.ctime()
#     outfile = os.path.join(settings.PROJECT_ROOT, 'celery_test.tmp')
#     with open(outfile, 'a') as f:
#         f.write("{0}\n".format(now))
#     return now
#
# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))