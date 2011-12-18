from django.http import Http404
from django.shortcuts import render
from aspc.folio.models import Page
from aspc.eatshop.models import Business

COOP_FOUNTAIN_ID = 1
COOP_FOUNTAIN_SLUG = "coop-fountain"

def coop_fountain(request):
    coop = Business.objects.on_campus().get(pk=COOP_FOUNTAIN_ID)
    page = Page.objects.get(slug="coop-fountain")
    
    return render(request, "eatshop/coop_fountain.html",
                  {'business': coop, 'page': page})

