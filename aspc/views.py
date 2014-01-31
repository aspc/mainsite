from django.views.generic.dates import ArchiveIndexView
from aspc.blog.views import PostArchive
from aspc.blog.models import Post
from aspc.events.models import EventController
from aspc.activityfeed.models import Activity
import logging, datetime

log = logging.getLogger(__name__)

class HomeView(PostArchive):
    template_name = "home.html"
    model = Post
    date_field = 'posted'
    context_object_name = 'posts'
    allow_empty = True
    paginate_by = 5 # show only 5 recent posts on homepage

    def get_queryset(self, *args, **kwargs):
        qs = super(HomeView, self).get_queryset(*args, **kwargs)
        qs = qs.select_related('author__user')
        return qs

    def get_context_data(self, **kwargs):
        num_activities = self.request.GET.get('num_activities', 10)
        try:
            num_activities = int(num_activities)
        except TypeError:
            num_activities = 10

        dtnow = datetime.datetime.now()
        qs_date_from = self.request.GET.get('from')
        qs_date_to = self.request.GET.get('to')

        if qs_date_from:
            try:
                date_from = datetime.datetime.strptime(qs_date_from, '%Y-%m-%d')
            except ValueError:
                date_from = dtnow.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            date_from = dtnow.replace(hour=0, minute=0, second=0, microsecond=0)

        if qs_date_to:
            try:
                date_to = datetime.datetime.strptime(qs_date_to, '%Y-%m-%d')
            except ValueError:
                date_to = date_from + datetime.timedelta(days=1)
        else:
            date_to = date_from + datetime.timedelta(days=1)

        context = super(HomeView, self).get_context_data(**kwargs)
        context['activities'] = Activity.objects.all()[:num_activities]
        context['all_nav'] = True
        context['events'] = EventController.approved_events().filter(
                                start__gte=date_from,
                                start__lt=date_to
                            )
        return context
