from django.views.generic.dates import (DateDetailView, ArchiveIndexView, 
    MonthArchiveView, _date_from_string)
from django.http import Http404
import datetime

class PostDetail(DateDetailView):
    def get_object(self):
        return self.model.objects.get(slug=self.kwargs['slug'].lower())

class PostMonthArchive(MonthArchiveView):
    def _previous_posts(self):
        year, month, day = self.get_year(), self.get_month(), '1'
        format = '{0}-{1}-{2}'.format(
            self.get_year_format(),
            self.get_month_format(),
            '%d'
        )
        timestr = '{0}-{1}-{2}'.format(year, month, day)
        month_start = datetime.datetime.strptime(timestr, format)
        
        return self.model.objects.filter(**{
            '{0}__lt'.format(self.date_field): month_start,
        })
    
    def get_context_data(self, **kwargs):
        context = super(PostMonthArchive, self).get_context_data(**kwargs)
        
        current_exists = context[self.get_context_object_name(self.model)].exists()
        previous_exists = self._previous_posts().exists()
        
        if (not current_exists) and (not previous_exists):
            raise Http404 # Nothing in this month, nothing prior to it,
                          # better bail
        elif not previous_exists:
            context['previous_posts_exist'] = False
        else:
            context['previous_posts_exist'] = True
        
        return context


class PostArchive(ArchiveIndexView):
    def get_context_data(self, **kwargs):
        context = super(PostArchive, self).get_context_data(**kwargs)
        qs = self.model.objects.all()
        if not self.allow_future:
            qs = qs.exclude(**{'{0}__gt'.format(self.date_field): datetime.datetime.now(),})
        qs = qs.values_list('posted', flat=True)
        years = set()
        for date in qs:
            years.add(date.year)
        context['years'] = years
        return context
