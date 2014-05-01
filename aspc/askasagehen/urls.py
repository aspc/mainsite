from django.conf.urls import patterns, url
from aspc.askasagehen.views import home

urlpatterns = patterns('',
	url(r'', home, name='askasagehen')
)