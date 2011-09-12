from django.conf.urls.defaults import patterns, include, url
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView,
    MonthArchiveView, DateDetailView)
from aspc.blog.models import Post
from aspc.blog.views import PostDetail, PostArchive

detail_kwargs = {
    'model': Post,
    'date_field': 'posted',
    'context_object_name': 'post',
}

post_kwargs = detail_kwargs.copy()
post_kwargs.update({
    'allow_empty': True,
    'context_object_name': 'posts',
})

urlpatterns = patterns('',
    url(r'^$', PostArchive.as_view(**post_kwargs), name="post_index"),
    url(r'^(?P<year>\d{4})/$', YearArchiveView.as_view(**post_kwargs), name="post_year"),
    url(r'^(?P<year>\d{4})/(?P<month>[^/]+)/$', MonthArchiveView.as_view(**post_kwargs), name="post_month"),
    url(r'^(?P<year>\d{4})/(?P<month>[^/]+)/(?P<slug>[A-Za-z0-9_-]+)/$', PostDetail.as_view(**detail_kwargs), name="post_detail"),
)
