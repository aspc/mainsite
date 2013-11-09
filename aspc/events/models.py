from django.db import models
from aspc.events.backends.facebook import FacebookBackend
from aspc.events.backends.collegiatelink import CollegiateLinkBackend
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
import logging

logger = logging.getLogger(__name__)

CHARFIELD_MAX_LENGTH = 255


class Event(models.Model):
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    description = models.TextField()
    host = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    url = models.CharField(max_length=CHARFIELD_MAX_LENGTH, null=True, blank=True)
    status = models.CharField(max_length=CHARFIELD_MAX_LENGTH, choices=(('pending', 'Pending'), ('approved', 'Approved'), ('denied', 'Denied')), default='pending')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('start', 'name', 'end')
        verbose_name_plural = "Events"

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
	def fetch_collegiatelink_events():
		cl = CollegiateLinkBackend()
		events_data = cl.get_events_data()

		for event_data in events_data:
			logger.debug(event_data['name'])
			#event = Event.objects.get_or_create(name=event_data['name'], defaults={'status': 'pending'})  # Updates an existing event or adds a new one to the database
			event = Event.objects.get_or_create(name=event_data['name'], status='pending')  # Updates an existing event or adds a new one to the database

			for key, value in event_data.items():
			    setattr(event, key, value)
			event.save()


		return events_data

	# GET methods invoked by views
	@staticmethod
	def all_events():
		return Event.objects.all()

	@staticmethod
	def approved_events():
		return Event.objects.all().filter(status='approved')

	@staticmethod
	def event_with_id(event_id):
		try:
			event = (EventController.approved_events()).get(id=event_id)
		except ObjectDoesNotExist:
			return None
		else:
			return event

	@staticmethod
	def todays_events():
		try:
			event = (EventController.approved_events()).filter(start__year=date.today().year, start__month=date.today().month, start__day=date.today().day)
		except ObjectDoesNotExist:
			return None
		else:
			return event
