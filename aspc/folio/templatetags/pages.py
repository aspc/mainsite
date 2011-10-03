from django import template
from aspc.folio.models import Page
import re

register = template.Library()

class BreadcrumbsListNode(template.Node):
    def __init__(self, leaf_page, var_name):
        self.leaf_page = template.Variable(leaf_page)
        self.var_name = var_name
    def render(self, context):
        context[self.var_name] = self.leaf_page.resolve(context).path()
        return ''

def do_breadcrumbs_list(parser, token):
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)
    leaf_page, var_name = m.groups()
    return BreadcrumbsListNode(leaf_page, var_name)

register.tag("breadcrumbs_list", do_breadcrumbs_list)

class NavigationListNode(template.Node):
    def __init__(self, root_names, var_name, exclude_pages):
        self.root_names = root_names
        self.exclude_pages = exclude_pages
        self.var_name = var_name
    def render(self, context):
        nav_pages = Page.objects.filter(parent__isnull=True).exclude(
            slug__in=self.exclude_pages)
        if self.root_names:
            nav_pages = nav_pages.filter(slug__in=self.root_names)
        top_pages = []
        
        for page in nav_pages:
            top_pages.append((page, page.page_set.all()))
        context[self.var_name] = top_pages
        return ''

def do_navigation_list(parser, token):
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
    m = re.search(r'(?:(\S+) )?as (\w+)(?: excluding (.*))?', arg)
    if not m:
        raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)
    root_names, var_name, exclude_pages = m.groups()
    
    if exclude_pages:
        exclude_pages = exclude_pages.split(',')
    else:
        exclude_pages = []
    
    if root_names:
        root_names = root_names.split(',')
    else:
        root_names = []
    
    return NavigationListNode(root_names, var_name, exclude_pages)

register.tag("root_navigation_list", do_navigation_list)