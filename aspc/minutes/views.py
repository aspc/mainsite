from django.views.generic.dates import DateDetailView, ArchiveIndexView
from django.http import Http404
import datetime

class MinutesDetail(DateDetailView):
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

class MinutesArchive(ArchiveIndexView):
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
