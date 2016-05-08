from django import template
from aspc.menu.models import Item

register = template.Library()

@register.filter
def image_url(value):
    item, created = Item.objects.get_or_create(name=value)
    return item.image_url