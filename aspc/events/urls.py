from django.conf.urls import patterns, url
from aspc.events.views import home

urlpatterns = patterns('',
	url(r'^$', home, name="events"),
)