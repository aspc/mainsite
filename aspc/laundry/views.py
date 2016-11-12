from django.shortcuts import render
from aspc.college.models import Building


def laundry_home(request):
    dorms = Building.objects.all()
    return render(request, "laundry_home.html", {'buildings': dorms})