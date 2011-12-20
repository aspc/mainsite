from django.http import Http404
from django.shortcuts import render
from django.views.generic.list import ListView
from aspc.folio.models import Page
from aspc.eatshop.models import Business
from aspc.eatshop.filters import (OnCampusFilterSet, RestaurantsFilterSet,
    AllBusinessesFilterSet)
from aspc.eatshop.config import COOP_FOUNTAIN_ID, COOP_FOUNTAIN_SLUG

def coop_fountain(request):
    coop = Business.objects.on_campus().get(pk=COOP_FOUNTAIN_ID)
    page = Page.objects.get(slug="coop-fountain")
    
    return render(request, "eatshop/coop_fountain.html",
                  {'business': coop, 'page': page})

def on_campus(request):
    f = OnCampusFilterSet(request.GET, queryset=Business.objects.on_campus())
    return render(request, 'eatshop/on_campus_list.html', {'filter': f})

def restaurants(request):
    f = RestaurantsFilterSet(request.GET, queryset=Business.objects.restaurants())
    return render(request, 'eatshop/restaurants_list.html', {'filter': f})

def home(request):
    f = AllBusinessesFilterSet(request.GET, queryset=Business.objects.all())
    return render(request, 'eatshop/all_businesses_list.html', {'filter': f})