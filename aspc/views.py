from django.views.generic.dates import ArchiveIndexView
from aspc.blog.models import Post

class HomeView(ArchiveIndexView):
    template_name = "home.html"
    model = Post
    date_field = 'posted'
    context_object_name = 'posts'
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['all_nav'] = True
        return context
    