from django.shortcuts import render

def mental_health_home(request):
    return render(request, "mental_health_home.html")
