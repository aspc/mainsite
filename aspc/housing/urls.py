from django.conf.urls.defaults import patterns, include, url
from aspc.housing.views import Home, RoomDetail, \
    BrowseBuildings, BrowseBuildingFloor, ReviewRoom, ReviewRoomWithChoice, search

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name="housing_home"),
    url(r'^search/$', search, name="housing_search"),
    url(r'^browse/$', BrowseBuildings.as_view(), name="housing_browse"),
    url(r'^review/$', ReviewRoomWithChoice.as_view(), name="housing_review"),
    url(r'^browse/(?P<building>[^\s/]+)/$', BrowseBuildingFloor.as_view(), name="housing_browse_building_floor_first"),
    url(r'^browse/(?P<building>[^\s/]+)/(?P<floor>\d)/$', BrowseBuildingFloor.as_view(), name="housing_browse_building_floor"),
    url(r'^browse/(?P<building>[^\s/]+)/(?P<floor>\d)/(?P<room>[A-Za-z0-9]+)/$', RoomDetail.as_view(), name="housing_browse_room"),
    url(r'^browse/(?P<building>[^\s/]+)/(?P<floor>\d)/(?P<room>[A-Za-z0-9]+)/review/$', ReviewRoom.as_view(), name="housing_review_room"),
)
