from django.shortcuts import render

from aspc.mentalhealth.models import Therapist

def home(request):
    therapists = Therapist.objects.all()
    return render(request, 'mentalhealth_home.html', {'therapists': therapists})
