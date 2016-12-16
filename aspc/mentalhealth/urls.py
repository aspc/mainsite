from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from aspc.mentalhealth.views import home, ReviewView, therapist

urlpatterns = [
    url(r'^$', home, name="mentalhealth_home"),
    url(r'^review/new/?$', ReviewView.as_view(), name="review_create"),
    url(r'^review/(?P<review_id>\d+)/?$', ReviewView.as_view(), name="review_edit"),
    url(r'^therapist/(?P<therapist_id>\d+)/?$', therapist, name="therapist"),
    #url(r'^review$', login_required(ReviewView.as_view()), name="review"),
]