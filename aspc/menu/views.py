from aspc.menu.models import Menu, Item
from django.shortcuts import render
from django.http import HttpResponseNotAllowed, HttpResponse
from datetime import datetime, date, timedelta
from aspc.settings import GOOGLE_SEARCH_KEY, GOOGLE_SEARCH_CX
import json, requests

# /menu
def home (request):
	if request.method == 'GET':
		if datetime.today().weekday() < 5:
			return weekday(request, datetime.today().strftime('%A')[:3].lower()) # Calls the render method with the appopriate weekday parameter
		else:
			return weekend(request, datetime.today().strftime('%A')[:3].lower()) # Calls the render method with the appopriate weekday parameter
	else:
		return HttpResponseNotAllowed(['GET'])

# /menu/{weekday}
def weekday (request, day):
	if request.method == 'GET':
		return render(request, 'menu/weekday_menu.html', {
			'current_week': _current_week(),
			'current_day': day,
			'current_date': _current_date(),
			'frank_meals': {
				'breakfast_items': _get_or_none(Menu.frank_meals, day=day, meal='breakfast'),
				'lunch_items': _get_or_none(Menu.frank_meals, day=day, meal='lunch'),
				'dinner_items': _get_or_none(Menu.frank_meals, day=day, meal='dinner')
			},
			'frary_meals': {
				'breakfast_items': _get_or_none(Menu.frary_meals, day=day, meal='breakfast'),
				'lunch_items': _get_or_none(Menu.frary_meals, day=day, meal='lunch'),
				'dinner_items': _get_or_none(Menu.frary_meals, day=day, meal='dinner')
			},
			'oldenborg_meals': {
				'lunch_items': _get_or_none(Menu.oldenborg_meals, day=day, meal='lunch'),
			},
			'scripps_meals': {
				'breakfast_items': _get_or_none(Menu.scripps_meals, day=day, meal='breakfast'),
				'lunch_items': _get_or_none(Menu.scripps_meals, day=day, meal='lunch'),
				'dinner_items': _get_or_none(Menu.scripps_meals, day=day, meal='dinner')
			},
			'mudd_meals': {
				'breakfast_items': _get_or_none(Menu.mudd_meals, day=day, meal='breakfast'),
				'lunch_items': _get_or_none(Menu.mudd_meals, day=day, meal='lunch'),
				'dinner_items': _get_or_none(Menu.mudd_meals, day=day, meal='dinner')
			},
			'cmc_meals': {
				'breakfast_items': _get_or_none(Menu.cmc_meals, day=day, meal='breakfast'),
				'lunch_items': _get_or_none(Menu.cmc_meals, day=day, meal='lunch'),
				'dinner_items': _get_or_none(Menu.cmc_meals, day=day, meal='dinner')
			},
			'pitzer_meals': {
				'breakfast_items': _get_or_none(Menu.pitzer_meals, day=day, meal='breakfast'),
				'lunch_items': _get_or_none(Menu.pitzer_meals, day=day, meal='lunch'),
				'dinner_items': _get_or_none(Menu.pitzer_meals, day=day, meal='dinner')
			}
		})
	else:
		return HttpResponseNotAllowed(['GET'])

# /menu/{weekend}
def weekend (request, day):
	if request.method == 'GET':
		return render(request, 'menu/weekend_menu.html', {
			'current_week': _current_week(),
			'current_day': day,
			'current_date': _current_date(),
			'frank_meals': {
				'brunch_items': _get_or_none(Menu.frank_meals, day=day, meal='brunch'),
				'dinner_items': _get_or_none(Menu.frank_meals, day=day, meal='dinner')
			},
			'frary_meals': {
				'brunch_items': _get_or_none(Menu.frary_meals, day=day, meal='brunch'),
				'dinner_items': _get_or_none(Menu.frary_meals, day=day, meal='dinner')
			},
			'scripps_meals': {
				'brunch_items': _get_or_none(Menu.scripps_meals, day=day, meal='brunch'),
				'dinner_items': _get_or_none(Menu.scripps_meals, day=day, meal='dinner')
			},
			'mudd_meals': {
				'brunch_items': _get_or_none(Menu.mudd_meals, day=day, meal='brunch'),
				'dinner_items': _get_or_none(Menu.mudd_meals, day=day, meal='dinner')
			},
			'cmc_meals': {
				'brunch_items': _get_or_none(Menu.cmc_meals, day=day, meal='brunch'),
				'dinner_items': _get_or_none(Menu.cmc_meals, day=day, meal='dinner')
			},
			'pitzer_meals': {
				'brunch_items': _get_or_none(Menu.pitzer_meals, day=day, meal='brunch'),
				'dinner_items': _get_or_none(Menu.pitzer_meals, day=day, meal='dinner')
			}
		})
	else:
		return HttpResponseNotAllowed(['GET'])

def get_image_url(name):
	GOOGLE_SEARCH_URL = 'https://www.googleapis.com/customsearch/v1?'
	params = {'q': name, 'key': GOOGLE_SEARCH_KEY, 'cx':GOOGLE_SEARCH_CX, 'num':1, 'searchType': "image"}
	resp = requests.get(url=GOOGLE_SEARCH_URL, params=params)
	data = json.loads(resp.text)
	return data['items'][0]['link']

def get_image(request):
	name = request.GET['name']
	i, created = Item.objects.get_or_create(name=name)
	if not i.image_url:
		url = str(get_image_url(i.name))
		i.image_url = url
		i.save()
	return HttpResponse(i.image_url)

# Helper function to prevent lookup errors on days when certain dining halls aren't serving
def _get_or_none(model_objects, **kwargs):
    try:
    	food_items = model_objects.get(**kwargs).food_items.all()
    	if food_items:
    		return food_items
    	else:
    		return ['No menu.']
    except Menu.DoesNotExist:
        return ['No menu.']

# Helper function to generate a string that represents the current weekday
def _current_week():
	today = date.today()
	this_monday = today - timedelta(days=today.weekday())
	this_sunday = this_monday + timedelta(days=6)
	return 'Week of {0} {1} to {2} {3}'.format(this_monday.strftime('%B'), this_monday.strftime('%d').lstrip('0'), this_sunday.strftime('%B'), this_sunday.strftime('%d').lstrip('0'))

# Helper function to generate a string a represents the current date
def _current_date():
	today = date.today()
	return today.strftime("%A, %B %d")