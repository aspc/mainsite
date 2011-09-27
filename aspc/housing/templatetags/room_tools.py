from django import template
from aspc.housing.models import Room

register = template.Library()

@register.inclusion_tag('housing/stars.html')
def show_stars(num):
    if num:
        return {'stars': '&#9733;&nbsp;'*int(num+1), 'number': int(num+1),}
    else:
        return {}

@register.inclusion_tag('housing/suite_snippet.html')
def suite(room):
    suite_rooms = Room.objects.filter(suite=room.suite)
    return {'suite_rooms': suite_rooms, 'room': room,}