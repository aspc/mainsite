from django.conf.urls.defaults import patterns, include, url
from aspc.folio.models import Page
from aspc.views import HomeView
from aspc.blog.urls import post_kwargs

from django.contrib import admin
admin.autodiscover()

# home_kwargs = post_kwargs.copy()
# home_kwargs.update({'template_name': 'home.html'})

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^news/', include('aspc.blog.urls')),
    url(r'^sagebooks/', include('aspc.sagelist.urls')),
    url(r'^accounts/', include('aspc.auth.urls')),
    url(r'^housing/', include('aspc.housing.urls')),
    (r'(?P<slug_path>(?:[\w\-\d]+/)+)$', 'aspc.folio.views.page_view',),
    # Examples:
    # url(r'^$', 'aspc.views.home', name='home'),
    # url(r'^aspc/', include('aspc.foo.urls')),
)
