from django.views.generic.dates import (DateDetailView, ArchiveIndexView,
    MonthArchiveView, _date_from_string)
from django.http import Http404
from aspc.generic import FilteredMonthArchiveView
import datetime
from aspc.blog.models import Post
from django.http import Http404

class PostDetail(DateDetailView):
    def get_object(self):
        try:
            return self.model.objects.get(slug=self.kwargs['slug'].lower())
        except Post.DoesNotExist:
            raise Http404

class PostMonthArchive(FilteredMonthArchiveView):
    pass

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
