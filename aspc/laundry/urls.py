from django.conf.urls import patterns, include, url
from aspc.laundry.views import laundry_home, laundry_machine


urlpatterns = [
    url(r'^$', laundry_home, name="laundry_home"),
    url(r'^(?P<pk>\d)/$', laundry_machine, name="laundry_machine"),
]