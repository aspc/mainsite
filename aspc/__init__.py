from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
## FIXME: Removed for Django 1.8 upgrade
# from .celery_setup import app as celery_app
