from django.db import models

CHARFIELD_MAX_LENGTH = 255

class Event(models.Model):
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    start = models.DateTimeField()
    end = models.DateTimeField()
    location = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    description = models.TextField()
    status = models.CharField(max_length=CHARFIELD_MAX_LENGTH) #  pending, approved, or denied

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('start', 'name', 'end')
        verbose_name_plural = "published events"