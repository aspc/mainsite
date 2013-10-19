from django.conf.urls import patterns, url
from aspc.events.views import home, event

urlpatterns = patterns('',
	url(r'^$', home, name="events"), # /events
	url(r'^(?P<event_id>\d+)(/)?', event) # /events/123
)