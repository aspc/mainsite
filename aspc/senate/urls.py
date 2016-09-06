from django.conf.urls import patterns, include, url
from aspc.senate.views import DocumentList, AppointmentList, PositionList

urlpatterns = [
    url(r'^documents/?$', DocumentList.as_view(), name="document_list"),
    url(r'^documents/(?P<page>[0-9]+)/?$', DocumentList.as_view(), name="document_list_page"),
    url(r'^positions/?$', PositionList.as_view(), name="positions"),
    url(r'^appointments/(?P<committee>[^/]+)/?$', AppointmentList.as_view(), name="appointments"),
]