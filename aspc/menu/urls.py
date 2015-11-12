from django.conf.urls import patterns, url, include
from aspc.menu.views import home, weekend, weekday

urlpatterns = [
	url(r'mon', weekday, {'day': 'mon'}, name='mon'),
	url(r'tue', weekday, {'day': 'tue'}, name='tue'),
	url(r'wed', weekday, {'day': 'wed'}, name='wed'),
	url(r'thu', weekday, {'day': 'thu'}, name='thu'),
	url(r'fri', weekday, {'day': 'fri'}, name='fri'),
	url(r'sat', weekend, {'day': 'sat'}, name='sat'),
	url(r'sun', weekend, {'day': 'sun'}, name='sun'),
	url(r'', home, name='menu')
]