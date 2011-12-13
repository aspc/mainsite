from django.conf.urls.defaults import patterns, include, url
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView,
    MonthArchiveView, DateDetailView)
from aspc.minutes.models import MeetingMinutes
from aspc.minutes.views import MinutesDetail, MinutesArchive

detail_kwargs = {
    'model': MeetingMinutes,
    'date_field': 'date',
    'context_object_name': 'minutes',
}

archive_kwargs = detail_kwargs.copy()
archive_kwargs.update({
    'allow_empty': True,
})

urlpatterns = patterns('',
    url(r'^$', MinutesArchive.as_view(**archive_kwargs), name="minutes_index"),
    url(r'^(?P<year>\d{4})/$', YearArchiveView.as_view(**archive_kwargs), name="minutes_year"),
    url(r'^(?P<year>\d{4})/(?P<month>[^/]+)/$', MonthArchiveView.as_view(**archive_kwargs), name="minutes_month"),
    url(r'^(?P<year>\d{4})/(?P<month>[^/]+)/(?P<day>\d+)/$', MinutesDetail.as_view(**detail_kwargs), name="minutes_detail"),
)
