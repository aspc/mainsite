from django.http import Http404
from django.shortcuts import render
from django.views.generic.list import ListView
from django.core.exceptions import ObjectDoesNotExist
from aspc.folio.models import Page
from aspc.eatshop.models import Business
from aspc.eatshop.filters import (OnCampusFilterSet, RestaurantsFilterSet,
    AllBusinessesFilterSet)
from aspc.eatshop.config import COOP_FOUNTAIN_ID, COOP_FOUNTAIN_SLUG
from django.views.decorators.cache import cache_page

def coop_fountain(request):
    try:
        page = Page.objects.get(slug=COOP_FOUNTAIN_SLUG)
    except Page.DoesNotExist:
        page = None

    try:
        coop = Business.objects.on_campus().get(pk=COOP_FOUNTAIN_ID)
    except Business.DoesNotExist:
        raise Http404

    return render(request, "eatshop/coop_fountain.html",
                  {'business': coop, 'page': page})

# Cache these pages for 24 hours
@cache_page(60 * 60 * 24)
def on_campus(request):
    f = OnCampusFilterSet(request.GET, queryset=Business.objects.on_campus())
    return render(request, 'eatshop/on_campus_list.html', {'filter': f})

@cache_page(60 * 60 * 24)
def restaurants(request):
    f = RestaurantsFilterSet(request.GET, queryset=Business.objects.restaurants())
    return render(request, 'eatshop/restaurants_list.html', {'filter': f})

@cache_page(60 * 60 * 24)
def businesses(request):
    f = AllBusinessesFilterSet(request.GET, queryset=Business.objects.non_food())
    return render(request, 'eatshop/businesses_list.html', {'filter': f})

@cache_page(60 * 60 * 24)
def home(request):
    f = AllBusinessesFilterSet(request.GET, queryset=Business.objects.all())
    return render(request, 'eatshop/all_businesses_list.html', {'filter': f})