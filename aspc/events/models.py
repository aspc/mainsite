from django.db import models
from aspc.events.backends.facebook import FacebookBackend
from aspc.events.backends.collegiatelink import CollegiateLinkBackend
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import time
import logging
import json

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


class FacebookEventPage(models.Model):
	name = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
	url = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
	page_id = models.CharField(max_length=CHARFIELD_MAX_LENGTH)

	def __unicode__(self):
	    return self.name

class FacebookEventPageController(object):
	def __unicode__(self):
	    return self.name

	@staticmethod
	def new_facebook_event_page(data):
		page_data = FacebookBackend().get_page_data(data['page_url'])

		# Updates an existing event page or adds a new one to the database
		# get_or_create returns an object and a boolean value specifying whether a new object was created or not
		event_page, is_new = FacebookEventPage.objects.get_or_create(name=page_data['name'])
		for key, value in page_data.items():
			setattr(event_page, key, value)
		event_page.save()

		FacebookEventPageController().scrape_page_events(event_page)

		return event_page

	@staticmethod
	def scrape_page_events(event_page):
		event_page_event_ids = FacebookBackend().get_page_event_ids(event_page.page_id)
		for event_id in event_page_event_ids:
			# Mimics raw data being passed via GET so we can reuse the new_event method
			normalized_event_data = {
				'event_source': 'facebook',
				'event_url': 'http://facebook.com/events/' + event_id
			}
			EventController().new_event(normalized_event_data)

	@staticmethod
	def facebook_event_pages():
		return FacebookEventPage.objects.all()


class EventController(object):
	def __unicode__(self):
	    return self.name

	@staticmethod
	def new_event(data):
		event_data = {}

		if data['event_source'] == 'facebook':
			event_data = FacebookBackend().get_event_data(data['event_url'])
		elif data['event_source'] == 'manual':
			event_data = data
			event_data['start'] = datetime.strptime(event_data['start'], '%Y-%m-%dT%H:%M')
			if 'end' in event_data and event_data['end'] != '':
				event_data['end'] = datetime.strptime(event_data['end'], '%Y-%m-%dT%H:%M')
			del event_data['event_source']
		else:  # If corrupted data or erroneous POST request, do nothing
			return False

		# Creates a new Event model with the data
		event = Event()
		for key, value in event_data.items():
			setattr(event, key, value)
		event.save()

		return event

	@staticmethod
	def fetch_collegiatelink_events():
		events_data = CollegiateLinkBackend().get_events_data()

		for event_data in events_data:
			# Updates an existing event or adds a new one to the database
			# get_or_create returns an object and a boolean value specifying whether a new object was created or not
			event, is_new = Event.objects.get_or_create(name=event_data['name'], defaults={'start': datetime.today(), 'status': 'pending'})

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
			event = (EventController.approved_events()).filter(start__year=datetime.today().year, start__month=datetime.today().month, start__day=datetime.today().day)
		except ObjectDoesNotExist:
			return None
		else:
			return event

class EventHelper(object):
	def __unicode__(self):
	    return self.name

	@staticmethod
	def earliest_event_time(event_list):
		start_times = [event.start.time() for event in event_list]
		if bool(len(start_times)):
			return min(start_times)
		else:
			return None

	@staticmethod
	def latest_event_time(event_list):
		start_times = [event.start.time() for event in event_list]
		if bool(len(start_times)):
			return max(start_times)
		else:
			return None

	@staticmethod
	def events_to_json(event_list):
		parsed_events = [];

		for event in event_list:
			s = '{'
			s += 'title: ' + json.dumps(event.name) + ', '
			s += 'start: ' + str(time.mktime(event.start.timetuple())) + ', '
			s += 'end: ' + (str(time.mktime(event.end.timetuple())) if event.end else 'null') + ', '
			s += 'location: ' + (json.dumps(event.location) if event.location else 'null') + ', '
			s += 'description: ' + (json.dumps(event.description) if event.description else 'null') + ', '
			s += 'url: "/events/event/' + str(event.id) + '", '
			s += 'allDay: false'
			s += '}'

			parsed_events.append(s)

		return '[' + ', '.join(parsed_events) + ']'