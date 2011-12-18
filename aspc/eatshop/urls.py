from django.conf.urls.defaults import patterns, include, url
from aspc.eatshop.models import Business
from aspc.eatshop.views import coop_fountain #, OnCampusList, RestaurantsList,
#     BusinessesList, BigList)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

home = {
    'queryset': Business.objects.all(),
    'template_name': 'eatshop/home.html',
}

on_campus = {
    'queryset': Business.objects.on_campus(),
}

restaurants = {
    'queryset': Business.objects.off_campus()
}

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(**home), name="eatshop"),
    url(r'^coop-fountain/$', coop_fountain, name="coop_fountain"),
    url(r'^on-campus/$', ListView.as_view(**on_campus), name="on_campus"),
    # url(r'^on-campus/$', OnCampusList.as_view(), name="on_campus"),
    # url(r'^on-campus/(?P<object_id>\d+)$', OnCampusDetail.as_view(), name="on_campus"),
    # url(r'^restaurants/$', RestaurantsList.as_view(), name="restaurants"),
    # url(r'^businesses/$', BusinessesList.as_view(), name="businesses"),
)
