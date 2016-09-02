from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from aspc.sagelist.views import (CreateBookSaleView, BookSaleDetailView,
    ListBookSalesView, ListCourseBookSalesView, ListUserBookSalesView, BookSaleDeleteView)

urlpatterns = [
    url(r'^$', ListBookSalesView.as_view(), name="sagelist"),
    url(r'^create/$', login_required(CreateBookSaleView.as_view()), name="sagelist_create"),
    url(r'^(?P<pk>\d+)/$', BookSaleDetailView.as_view(), name="sagelist_detail"),
    url(r'^(?P<pk>\d+)/delete/$', BookSaleDeleteView.as_view(), name="sagelist_delete"),
    url(r'^course/(?P<course_id>\d+)/', ListCourseBookSalesView.as_view(), name="sagelist_course_listings"),
    url(r'^(?P<email>[^/]+)/$', ListUserBookSalesView.as_view(), name="sagelist_user_listings"),
]