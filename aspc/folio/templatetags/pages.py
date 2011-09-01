from django import template
import re

register = template.Library()

class BreadcrumbsListNode(template.Node):
    def __init__(self, leaf_page, var_name):
        self.leaf_page = template.Variable(leaf_page)
        self.var_name = var_name
    def render(self, context):
        page = self.leaf_page.resolve(context)
        page_path = [page,]
        
        while page.parent:
            page = page.parent
            page_path.append(page)
        
        page_path.reverse()
        
        context[self.var_name] = page_path
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