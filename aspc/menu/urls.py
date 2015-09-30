from django.conf.urls import patterns, url, include
from rest_framework.authtoken import views
from aspc.menu.views import home, weekend, weekday
from aspc.menu.api.views import MenuList, MenuDiningHallDetail, MenuDayDetail, MenuDiningHallDayDetail, MenuDiningHallDayMealDetail

urlpatterns = [
    url(r'api/dining_hall/(?P<dining_hall>[^/]+)/day/(?P<day>[^/]+)/meal/(?P<meal>[^/]+)', MenuDiningHallDayMealDetail.as_view()),
    url(r'api/dining_hall/(?P<dining_hall>[^/]+)/day/(?P<day>[^/]+)', MenuDiningHallDayDetail.as_view()),
    url(r'api/day/(?P<day>[^/]+)', MenuDayDetail.as_view()),
    url(r'api/dining_hall/(?P<dining_hall>[^/]+)', MenuDiningHallDetail.as_view()),
    url(r'api', MenuList.as_view(), name='api'),
    url(r'auth', views.obtain_auth_token),
	url(r'mon', weekday, {'day': 'mon'}, name='mon'),
	url(r'tue', weekday, {'day': 'tue'}, name='tue'),
	url(r'wed', weekday, {'day': 'wed'}, name='wed'),
	url(r'thu', weekday, {'day': 'thu'}, name='thu'),
	url(r'fri', weekday, {'day': 'fri'}, name='fri'),
	url(r'sat', weekend, {'day': 'sat'}, name='sat'),
	url(r'sun', weekend, {'day': 'sun'}, name='sun'),
	url(r'', home, name='menu')
]