from aspc.folio.models import Page

def page_dispatch(request, slug_path, section):
    '''slug_path: ^(?P<slug_path>(?:[\w\-\d]+/)+)$ '''
    slug_parts = slug_path.rstrip('/').split('/')
    pages = Page.objects.filter(section=section)
    for part in slug_parts:
        try:
            new_page = pages.get(slug=part)
        except Page.DoesNotExist:
            raise Http404
        else:
            pages = new_page.page_set.all()
    