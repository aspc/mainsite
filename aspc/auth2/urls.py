from django.conf.urls import patterns, url
from aspc.auth2.views import guest_login, login, logout

urlpatterns = patterns('',
	url(r'^guest_login/$', guest_login, name="guest_login"),
	url(r'^login/$', login, name="login"),
    url(r'^logout/$', logout, name="logout"),
)
