from django import template
from aspc.housing.models import Room

register = template.Library()

@register.inclusion_tag('housing/stars.html')
def show_stars(num):
    return {'stars': '&#10025;&nbsp;'*int(num+1), 'number': int(num+1),}

@register.inclusion_tag('housing/suite_snippet.html')
def suite(room):
    suite_rooms = Room.objects.filter(suite=room.suite)
    return {'suite_rooms': suite_rooms, 'room': room,}