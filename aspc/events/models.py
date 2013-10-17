from django.db import models
from aspc.events.backends.facebook import FacebookBackend

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

class EventController(object):
	def __unicode__(self):
	    return self.name

	@staticmethod
	def new_event(data):
		fb = FacebookBackend()
		if data['event_source'] == 'facebook':
		    event_data = fb.get_event_data(data['event_url'])

		    event = Event()

		    for key, value in event_data.items():
		        setattr(event, key, value)

		    # Creates a new Event model with the Facebook data
		    event.save()

		    return event
		else:
			return False

	@staticmethod
	def all_events():
		return Event.objects.all()