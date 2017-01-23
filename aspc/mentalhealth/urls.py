from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from aspc.mentalhealth.views import home, ReviewView, therapist

urlpatterns = [
    url(r'^$', home, name="mentalhealth_home"),
    url(r'^therapist/(?P<therapist_id>\d+)/review/?$', login_required(ReviewView.as_view()), name="therapist_review"),
    url(r'^therapist/(?P<therapist_id>\d+)/?$', therapist, name="therapist"),
]