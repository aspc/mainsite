from django.conf.urls import patterns, url
from aspc.menu.views import home, weekend, weekday

urlpatterns = patterns('',
	url(r'', home, name='menu'),
	url(r'mon', weekday, name='mon'),
	url(r'tue', weekday, name='tue'),
	url(r'wed', weekday, name='wed'),
	url(r'thu', weekday, name='thu'),
	url(r'fri', weekday, name='fri'),
	url(r'sat', weekend, name='sat'),
	url(r'sun', weekend, name='sun')
)