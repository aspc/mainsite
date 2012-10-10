from django.views.generic.dates import ArchiveIndexView
from aspc.blog.views import PostArchive
from aspc.blog.models import Post
import logging, datetime

log = logging.getLogger(__name__)

class HomeView(PostArchive):
    template_name = "home.html"
    model = Post
    date_field = 'posted'
    context_object_name = 'posts'
    allow_empty = True
    
    def get_queryset(self, *args, **kwargs):
        qs = super(HomeView, self).get_queryset(*args, **kwargs)
        qs = qs.select_related('author__user')
        return qs
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['all_nav'] = True
        return context
    