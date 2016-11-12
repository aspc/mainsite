from django.shortcuts import render
from aspc.college.models import Building
from aspc.laundry.models import LaundryMachine


def laundry_home(request):
    dorms = Building.objects.all()
    return render(request, "laundry_home.html", {'buildings': dorms})

def laundry_machine(request, pk):
    machine = LaundryMachine.objects.get(pk=pk)
    return render(request, "laundry_machine.html", {'machine': machine})