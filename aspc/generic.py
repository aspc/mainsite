from django.views.generic.dates import MonthArchiveView
from django.http import Http404
import datetime

class FilteredMonthArchiveView(MonthArchiveView):
    """
    Prevent the month archives from going back past the first post, even
    when `allow_empty` is True.
    
    Adds a context variable `previous_posts_exist` to let the template
    decide whether to show a link to a previous month.
    """
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
        context = super(FilteredMonthArchiveView, self).get_context_data(**kwargs)
        
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