from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aspc.settings')

app = Celery('aspc')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(CELERYBEAT_SCHEDULE={
    "update-catalog": {
        "task": "aspc.coursesearch.tasks.smart_update",
        # Full catalog refresh finishes by 5am typically
        "schedule": crontab(hour=5),
    },
    "update-enrollments": {
        "task": "aspc.coursesearch.tasks.smart_update",
        # Looks like the actual time the refresh finishes drifts
        # but it's usually done by 20 after the hour
        "schedule": crontab(hour="*", minute=20),
    },
})


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
