from django.conf.urls import patterns, url, include
from aspc.api import views
from aspc.api.views import MenuList, MenuDiningHallDetail, MenuDayDetail, MenuDiningHallDayDetail, MenuDiningHallDayMealDetail

urlpatterns = [
    url(r'menu/dining_hall/(?P<dining_hall>[^/]+)/day/(?P<day>[^/]+)/meal/(?P<meal>[^/]+)/$', MenuDiningHallDayMealDetail.as_view()),
    url(r'menu/dining_hall/(?P<dining_hall>[^/]+)/day/(?P<day>[^/]+)/$', MenuDiningHallDayDetail.as_view()),
    url(r'menu/day/(?P<day>[^/]+)/$', MenuDayDetail.as_view()),
    url(r'menu/dining_hall/(?P<dining_hall>[^/]+)/$', MenuDiningHallDetail.as_view()),
    url(r'menu/$', MenuList.as_view()),
    url(r'^$', views.api_home, name="api_home"),
]