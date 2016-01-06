from django.conf.urls import patterns, include, url
from django.conf import settings
from aspc.folio.models import Page
from aspc.views import HomeView
from aspc.blog.urls import post_kwargs
from django.http import HttpResponseRedirect
from django.contrib import admin
import debug_toolbar

# home_kwargs = post_kwargs.copy()
# home_kwargs.update({'template_name': 'home.html'})

urlpatterns = [
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('aspc.api.urls')),
    url(r'^news/', include('aspc.blog.urls')),
    url(r'^eatshop/', include('aspc.eatshop.urls')),
    url(r'^events/', include('aspc.events.urls')),
    url(r'^senate/meetings-and-minutes/', include('aspc.minutes.urls')),
    url(r'^senate/', include('aspc.senate.urls')),
    url(r'^sagebooks/', include('aspc.sagelist.urls')),
    url(r'^accounts/', include('aspc.auth2.urls')),
    url(r'^housing/', include('aspc.housing.urls')),
    url(r'^courses/', include('aspc.courses.urls')),
    url(r'^menu/', include('aspc.menu.urls')),
    url(r'^rideshare/', lambda request: HttpResponseRedirect('http://5crideshare.com')),
    url(r'(?P<slug_path>(?:[\w\-\d]+/)+)$', 'aspc.folio.views.page_view', name="folio_page"),
    url(r'^__debug__/', include(debug_toolbar.urls)),
]

if settings.DEBUG:
    urlpatterns.append(
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
    )