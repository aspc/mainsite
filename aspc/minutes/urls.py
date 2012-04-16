from django.conf.urls import patterns, include, url
from aspc.minutes.models import MeetingMinutes
from aspc.minutes.views import (MinutesDetail, MinutesArchive,
    MinutesYearArchiveView, MinutesMonthArchiveView)

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
    url(r'^(?P<year>\d{4})/$', MinutesYearArchiveView.as_view(**archive_kwargs), name="minutes_year"),
    url(r'^(?P<year>\d{4})/(?P<month>[^/]+)/$', MinutesMonthArchiveView.as_view(**archive_kwargs), name="minutes_month"),
    url(r'^(?P<year>\d{4})/(?P<month>[^/]+)/(?P<day>\d+)/$', MinutesDetail.as_view(**detail_kwargs), name="minutes_detail"),
)
