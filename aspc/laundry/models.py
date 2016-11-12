from aspc.college.models import Building
from datetime import datetime

from django.db import models

STATUSES = ((1, u'OCCUPIED'), (0, u'AVAILABLE'))

class LaundryMachine(models.Model):
    building = models.ForeignKey(Building)
    name = models.CharField(max_length=3)
    status = models.SmallIntegerField(choices=STATUSES)

    def last_change_time(self):
        changes = StatusChange.objects.filter(machine=self).order_by('-timestamp')
        if not changes:
            return None
        return changes[0].timestamp

class StatusChange(models.Model):
    machine = models.ForeignKey(LaundryMachine)
    new_status = models.SmallIntegerField(choices=STATUSES)
    timestamp = models.DateTimeField(default=datetime.now)

