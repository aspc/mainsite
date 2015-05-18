from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'auth/login.html',}, name="login"),
    url(r'^logout/$', logout, {'template_name': 'auth/logged_out.html',}, name="logout"),
]