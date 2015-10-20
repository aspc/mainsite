from django.conf.urls import patterns, url, include
from rest_framework.authtoken import views
from aspc.api.views import MenuList, MenuDiningHallDetail, MenuDayDetail, MenuDiningHallDayDetail, MenuDiningHallDayMealDetail

urlpatterns = [
    url(r'menu/dining_hall/(?P<dining_hall>[^/]+)/day/(?P<day>[^/]+)/meal/(?P<meal>[^/]+)', MenuDiningHallDayMealDetail.as_view()),
    url(r'menu/dining_hall/(?P<dining_hall>[^/]+)/day/(?P<day>[^/]+)', MenuDiningHallDayDetail.as_view()),
    url(r'menu/day/(?P<day>[^/]+)', MenuDayDetail.as_view()),
    url(r'menu/dining_hall/(?P<dining_hall>[^/]+)', MenuDiningHallDetail.as_view()),
    url(r'menu', MenuList.as_view(), name='api'),
    url(r'auth', views.obtain_auth_token)
]