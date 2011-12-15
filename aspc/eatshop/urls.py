from django.conf.urls.defaults import patterns, include, url
from aspc.eatshop.views import (coop_fountain, OnCampusList, RestaurantsList,
    BusinessesList)

urlpatterns = patterns('',
    url(r'^coop-fountain/$', coop_fountain, name="coop_fountain"),
    url(r'^on-campus/$', OnCampusList.as_view(), name="on_campus"),
    url(r'^restaurants/$', RestaurantsList.as_view(), name="restaurants"),
    url(r'^businesses/$', BusinessesList.as_view(), name="businesses"),
)
