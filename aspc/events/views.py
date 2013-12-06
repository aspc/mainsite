from django.shortcuts import render
from aspc.events.models import EventController, EventHelper
from django.http import HttpResponse
import urlparse
from django.core import serializers

# /events
def home (request):
	if request.method == 'GET':
		events = EventController.approved_events()
		return render(request, 'events/home.html', {'events': events, 'earliest_event_time': EventHelper.earliest_event_time(events), 'latest_event_time': EventHelper.latest_event_time(events)}) # Render the events index on GET
	elif request.method == 'POST':
		new_event = EventController.new_event(dict(urlparse.parse_qsl(request.body))) # Add an event manually on POST
		return HttpResponse(serializers.serialize('json', [new_event])) # Return a JSON hash of the new event

# /events/event/123
def event (request, event_id):
	if request.method == 'GET':
		event = EventController.event_with_id(event_id)

		if not event:
			return render(request, 'events/error.html', {'event_id': event_id})
		else:
			return render(request, 'events/event_description.html', {'event': event})

# /events/facebook_page
def facebook_page (request):
	if request.method == 'POST':
		new_event_page = EventController.new_event_facebook_page(dict(urlparse.parse_qsl(request.body)))
		return HttpResponse(serializers.serialize('json', [new_event_page])) # Return a JSON hash of the new event page