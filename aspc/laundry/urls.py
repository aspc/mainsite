from django.conf.urls import patterns, include, url
from aspc.laundry.views import laundry_home


urlpatterns = [
    url(r'^$', laundry_home, name="laundry_home"),
]