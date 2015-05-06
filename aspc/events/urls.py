from django.conf.urls import patterns, url
from aspc.events.views import home, event, facebook_page

urlpatterns = [
	url(r'^$', home, name="events"), # /events
	url(r'^event/(?P<event_id>\d+)?(/)?', event, name="events_detail"), # /events/123
	url('facebook_page', facebook_page) # /events/facebook_page
]

# REST structure
# aspc.pomona.edu/events is the app homepage
# aspc.pomona.edu/events/event/123 is an event resource
# aspc.pomona.edu/events/facebook_page/123 is a facebook_page resource