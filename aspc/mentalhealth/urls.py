from django.conf.urls import patterns, include, url
from aspc.mentalhealth.views import mental_health_home


urlpatterns = [
    url(r'^$', mental_health_home, name="mental_health_home"),
]