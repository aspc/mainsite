from django.shortcuts import render
from datetime import datetime

# /menu
def home (request):
	if request.method == 'GET':
		if datetime.today().weekday() < 5:
			return weekday(request)
		else:
			return weekend(request)

# /menu/{weekday}
def weekday (request):
	if request.method == 'GET':
		return render(request, 'menu/weekday_menu.html')

# /menu/{weekend}
def weekend (request):
	if request.method == 'GET':
		return render(request, 'menu/weekend_menu.html')