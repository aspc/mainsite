from django.conf.urls import patterns, url
from aspc.menu.views import home

urlpatterns = patterns('',
	url(r'^$', home, name="menu")
)