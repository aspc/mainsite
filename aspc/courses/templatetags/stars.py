from django import template
import math
from django.utils.safestring import mark_safe
from aspc.settings import STATIC_URL
from aspc.courses.models import POSSIBLE_GRADES

register = template.Library()

@register.filter
def star(rating):
    num_star_on = int(math.floor(rating))
    num_star_half = int(round(rating)) - num_star_on
    num_star_off = 5 - num_star_on - num_star_half

    html = num_star_on * ('<img height=15 src="'+STATIC_URL+'images/star-filled.png">') + \
        num_star_half * ('<img height=15 src="'+STATIC_URL+'images/star-half.png">') + \
        num_star_off * ('<img height=15 src="'+STATIC_URL+'images/star-empty.png">')
    return mark_safe(html)

@register.filter
def blue_star(rating):
    num_star_on = int(math.floor(rating))
    num_star_half = int(round(rating)) - num_star_on
    num_star_off = 5 - num_star_on - num_star_half

    html = num_star_on * ('<img height=15 src="'+STATIC_URL+'images/blue_star_full.png">') + \
        num_star_half * ('<img height=15 src="'+STATIC_URL+'images/blue_star_half.png">') + \
        num_star_off * ('<img height=15 src="'+STATIC_URL+'images/blue_star_empty.png">')
    return mark_safe(html)

@register.filter
def grade(rating):
    grades = dict(POSSIBLE_GRADES)
    return grades[rating]