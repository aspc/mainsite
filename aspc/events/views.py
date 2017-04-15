from django.shortcuts import render
from aspc.events.models import EventController, FacebookEventPageController, EventHelper
from django.http import HttpResponse, HttpResponseNotAllowed
import urlparse
from django.core import serializers
from aspc.events.exceptions import InvalidEventException, InvalidFacebookEventPageException, EventAlreadyExistsException

# /events
def home (request):
	if request.method == 'GET': # Render the events index on GET
		events = EventController.approved_events()
		weeks_events = EventController.weeks_events()
		return render(request, 'events/home.html', {
			'events': EventHelper.events_to_json(events),
			'earliest_event_time': EventHelper.earliest_event_time(weeks_events),
			'latest_event_time': EventHelper.latest_event_time(weeks_events),
			'facebook_event_pages': FacebookEventPageController.facebook_event_pages()
		})
	else:
		return HttpResponseNotAllowed(['GET'])

# /events/event/123
def event (request, event_id):
	if request.method == 'GET': # Render an event page for the corresponding event_id on GET
		event = EventController.event_with_id(event_id)

		if not event:
			return render(request, 'events/error.html', {'event_id': event_id})
		else:
			return render(request, 'events/event_description.html', {'event': event})
	elif request.method == 'POST': # Add an event manually on POST
		try:
			new_event = EventController.new_event(dict(urlparse.parse_qsl(request.body)))
		except (InvalidEventException, InvalidFacebookEventPageException, EventAlreadyExistsException) as e:
			return HttpResponse(
				content=e.error_message,
				status=500
			)

		return HttpResponse(serializers.serialize('json', [new_event])) # Return a JSON hash of the new event
	else:
		return HttpResponseNotAllowed(['GET', 'POST'])

# /events/facebook_page
def facebook_page (request):
	if request.method == 'POST':
		try:
			new_event_page = FacebookEventPageController.new_facebook_event_page(dict(urlparse.parse_qsl(request.body)))
		except InvalidEventException: # Display no error since it's not the submitter's fault that the page has malformed events
			pass
		except InvalidFacebookEventPageException as e:
			return HttpResponse(
				content=e.error_message,
				status=500
			)
		return HttpResponse(serializers.serialize('json', [new_event_page])) # Return a JSON hash of the new event page
	else:
		return HttpResponseNotAllowed(['POST'])
