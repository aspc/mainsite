from django.conf.urls import patterns, url
from aspc.auth2.views import login, logout

urlpatterns = patterns('',
	url(r'^login/$', login, name="login"),
    url(r'^logout/$', logout, name="logout"),
)
