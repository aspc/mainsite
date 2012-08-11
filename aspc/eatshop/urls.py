from django.conf.urls import patterns, include, url
from aspc.eatshop.models import Business
from aspc.eatshop.views import (coop_fountain, on_campus, 
    restaurants, home, businesses)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

# home = {
#     'queryset': Business.objects.all(),
#     'template_name': 'eatshop/home.html',
# }
# 
# on_campus = {
#     'queryset': Business.objects.on_campus(),
#     'template_name_suffix': '_list_on_campus',
# }
# 
# on_campus_detail = dict(on_campus)
# on_campus_detail['template_name_suffix'] = '_detail_on_campus'
# 
# restaurants = {
#     'queryset': Business.objects.restaurants(),
#     'template_name_suffix': '_list_restaurants',
# }
# 
# restaurants_detail = dict(restaurants)
# restaurants_detail['template_name_suffix'] = '_detail_restaurants'
# 
# non_food = {
#     'queryset': Business.objects.non_food(),
#     'template_name_suffix': '_list_non_food',
# }
# 
# non_food_detail = dict(restaurants)
# non_food_detail['template_name_suffix'] = '_detail_non_food'

urlpatterns = patterns('',
    url(r'^$', home, name="eatshop"),
    url(r'^coop-fountain/$', coop_fountain, name="coop_fountain"),
    url(r'^on-campus/$', on_campus, name="on_campus"),
    # url(r'^on-campus/$', OnCampusList.as_view(), name="on_campus"),
    # url(r'^on-campus/(?P<pk>\d+)/$', DetailView.as_view(**on_campus_detail), name="on_campus_detail"),
    url(r'^restaurants/$', restaurants, name="restaurants"),
    url(r'^businesses/$', businesses, name="businesses"),
)
