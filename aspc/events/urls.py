from django.conf.urls import patterns, url
from aspc.events.views import home, event, facebook_page

urlpatterns = patterns('',
	url(r'^$', home, name="events"), # /events
	url(r'^(?P<event_id>\d+)(/)?', event), # /events/123
	url('facebook_page', facebook_page) # /events/123
)