from django import template
from HTMLParser import HTMLParser
register = template.Library()

h = HTMLParser()

@register.filter
def clean_item_name(s):
    return h.unescape(s)