from aspc.menu.models import Menu
from django.shortcuts import render
from datetime import datetime

# /menu
def home (request):
	if request.method == 'GET':
		if datetime.today().weekday() < 5:
			return weekday(request, datetime.today().strftime('%A')[:3].lower()) # Calls the render method with the appopriate weekday parameter
		else:
			return weekend(request, datetime.today().strftime('%A')[:3].lower()) # Calls the render method with the appopriate weekday parameter

# /menu/{weekday}
def weekday (request, day):
	if request.method == 'GET':
		return render(request, 'menu/weekday_menu.html', {
			'frank_meals': {
				'breakfast': Menu.frank_meals.get(day=day, meal='breakfast'),
				'lunch': Menu.frank_meals.get(day=day, meal='lunch'),
				'dinner': Menu.frank_meals.get(day=day, meal='dinner')
			},
			'frary_meals': {
				'breakfast': Menu.frary_meals.get(day=day, meal='breakfast'),
				'lunch': Menu.frary_meals.get(day=day, meal='lunch'),
				'dinner': Menu.frary_meals.get(day=day, meal='dinner')
			},
			'oldenborg_meals': {
				'lunch': Menu.oldenborg_meals.get(day=day, meal='lunch')
			},
			'scripps_meals': {
				'breakfast': Menu.scripps_meals.get(day=day, meal='breakfast'),
				'lunch': Menu.scripps_meals.get(day=day, meal='lunch'),
				'dinner': Menu.scripps_meals.get(day=day, meal='dinner')
			},
			'mudd_meals': {
				'breakfast': Menu.mudd_meals.get(day=day, meal='breakfast'),
				'lunch': Menu.mudd_meals.get(day=day, meal='lunch'),
				'dinner': Menu.mudd_meals.get(day=day, meal='dinner')
			},
			'cmc_meals': {
				'breakfast': Menu.cmc_meals.get(day=day, meal='breakfast'),
				'lunch': Menu.cmc_meals.get(day=day, meal='lunch'),
				'dinner': Menu.cmc_meals.get(day=day, meal='dinner')
			},
			'pitzer_meals': {
				'lunch': Menu.pitzer_meals.get(day=day, meal='lunch'),
				'dinner': Menu.pitzer_meals.get(day=day, meal='dinner')
			}
		})

# /menu/{weekend}
def weekend (request, day):
	if request.method == 'GET':
		return render(request, 'menu/weekend_menu.html', {
			'frank_meals': {
				'brunch': Menu.frank_meals.get(day=day, meal='lunch'),
				'dinner': Menu.frank_meals.get(day=day, meal='dinner')
			},
			'frary_meals': {
				'brunch': Menu.frary_meals.get(day=day, meal='lunch'),
				'dinner': Menu.frary_meals.get(day=day, meal='dinner')
			},
			'oldenborg_meals': {
				'brunch': Menu.oldenborg_meals.get(day=day, meal='lunch'),
				'dinner': Menu.oldenborg_meals.get(day=day, meal='dinner')
			},
			'scripps_meals': {
				'brunch': Menu.scripps_meals.get(day=day, meal='lunch'),
				'dinner': Menu.scripps_meals.get(day=day, meal='dinner')
			},
			'mudd_meals': {
				'brunch': Menu.mudd_meals.get(day=day, meal='lunch'),
				'dinner': Menu.mudd_meals.get(day=day, meal='dinner')
			},
			'cmc_meals': {
				'brunch': Menu.cmc_meals.get(day=day, meal='lunch'),
				'dinner': Menu.cmc_meals.get(day=day, meal='dinner')
			},
			'pitzer_meals': {
				'brunch': Menu.pitzer_meals.get(day=day, meal='lunch'),
				'dinner': Menu.pitzer_meals.get(day=day, meal='dinner')
			}
		})