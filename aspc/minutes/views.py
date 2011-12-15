from django.views.generic.dates import (ArchiveIndexView, YearArchiveView,
    MonthArchiveView, DateDetailView)
from django.http import Http404
from aspc.folio.models import Page
from aspc.folio.views import AttachedPageMixin
import datetime

class MinutesPageMixin(AttachedPageMixin):
    page_slug = "meetings-and-minutes"

class MinutesYearArchiveView(MinutesPageMixin, YearArchiveView):
    pass

class MinutesMonthArchiveView(MinutesPageMixin, MonthArchiveView):
    pass

class MinutesDetail(MinutesPageMixin, DateDetailView):
    def get_object(self):
        # Parse date into datetime (or raise 404)
        try:
            minutes_date = datetime.datetime.strptime(
                "{month} {day} {year}".format(
                    month=self.kwargs['month'],
                    day=self.kwargs['day'],
                    year=self.kwargs['year']),
                "%b %d %Y"
            ).date()
        except:
            raise Http404
        try:
            return self.model.objects.get(date=minutes_date)
        except self.model.DoesNotExist:
            raise Http404

class MinutesArchive(MinutesPageMixin, ArchiveIndexView):
    def get_context_data(self, **kwargs):
        context = super(MinutesArchive, self).get_context_data(**kwargs)
        qs = self.model.objects.all()
        if not self.allow_future:
            qs = qs.exclude(**{'{0}__gt'.format(self.date_field): datetime.datetime.now(),})
        qs = qs.values_list('date', flat=True)
        years = set()
        for date in qs:
            years.add(date.year)
        context['years'] = years
        return context
