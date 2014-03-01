from aspc.menu.models import Menu
from django.shortcuts import render
from datetime import datetime, date, timedelta

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
			'current_week': _current_week(),
			'current_day': day,
			'frank_meals': {
				'breakfast': _get_or_none(Menu.frank_meals, day=day, meal='breakfast'),
				'lunch': _get_or_none(Menu.frank_meals, day=day, meal='lunch'),
				'dinner': _get_or_none(Menu.frank_meals, day=day, meal='dinner')
			},
			'frary_meals': {
				'breakfast': _get_or_none(Menu.frary_meals, day=day, meal='breakfast'),
				'lunch': _get_or_none(Menu.frary_meals, day=day, meal='lunch'),
				'dinner': _get_or_none(Menu.frary_meals, day=day, meal='dinner')
			},
			'oldenborg_meals': {
				'breakfast': _get_or_none(Menu.oldenborg_meals, day=day, meal='breakfast'),
				'lunch': _get_or_none(Menu.oldenborg_meals, day=day, meal='lunch'),
				'dinner': _get_or_none(Menu.oldenborg_meals, day=day, meal='dinner')
			},
			'scripps_meals': {
				'breakfast': _get_or_none(Menu.scripps_meals, day=day, meal='breakfast'),
				'lunch': _get_or_none(Menu.scripps_meals, day=day, meal='lunch'),
				'dinner': _get_or_none(Menu.scripps_meals, day=day, meal='dinner')
			},
			'mudd_meals': {
				'breakfast': _get_or_none(Menu.mudd_meals, day=day, meal='breakfast'),
				'lunch': _get_or_none(Menu.mudd_meals, day=day, meal='lunch'),
				'dinner': _get_or_none(Menu.mudd_meals, day=day, meal='dinner')
			},
			'cmc_meals': {
				'breakfast': _get_or_none(Menu.cmc_meals, day=day, meal='breakfast'),
				'lunch': _get_or_none(Menu.cmc_meals, day=day, meal='lunch'),
				'dinner': _get_or_none(Menu.cmc_meals, day=day, meal='dinner')
			},
			'pitzer_meals': {
				'breakfast': _get_or_none(Menu.pitzer_meals, day=day, meal='breakfast'),
				'lunch': _get_or_none(Menu.pitzer_meals, day=day, meal='lunch'),
				'dinner': _get_or_none(Menu.pitzer_meals, day=day, meal='dinner')
			}
		})

# /menu/{weekend}
def weekend (request, day):
	if request.method == 'GET':
		return render(request, 'menu/weekend_menu.html', {
			'current_week': _current_week(),
			'current_day': day,
			'frank_meals': {
				'brunch': _get_or_none(Menu.frank_meals, day=day, meal='brunch'),
				'dinner': _get_or_none(Menu.frank_meals, day=day, meal='dinner')
			},
			'frary_meals': {
				'brunch': _get_or_none(Menu.frary_meals, day=day, meal='brunch'),
				'dinner': _get_or_none(Menu.frary_meals, day=day, meal='dinner')
			},
			'oldenborg_meals': {
				'brunch': _get_or_none(Menu.oldenborg_meals, day=day, meal='brunch'),
				'dinner': _get_or_none(Menu.oldenborg_meals, day=day, meal='dinner')
			},
			'scripps_meals': {
				'brunch': _get_or_none(Menu.scripps_meals, day=day, meal='brunch'),
				'dinner': _get_or_none(Menu.scripps_meals, day=day, meal='dinner')
			},
			'mudd_meals': {
				'brunch': _get_or_none(Menu.mudd_meals, day=day, meal='brunch'),
				'dinner': _get_or_none(Menu.mudd_meals, day=day, meal='dinner')
			},
			'cmc_meals': {
				'brunch': _get_or_none(Menu.cmc_meals, day=day, meal='brunch'),
				'dinner': _get_or_none(Menu.cmc_meals, day=day, meal='dinner')
			},
			'pitzer_meals': {
				'brunch': _get_or_none(Menu.pitzer_meals, day=day, meal='brunch'),
				'dinner': _get_or_none(Menu.pitzer_meals, day=day, meal='dinner')
			}
		})

# Helper function to prevent lookup errors on days when certain dining halls aren't serving
def _get_or_none(model_objects, **kwargs):
    try:
        return model_objects.get(**kwargs)
    except Menu.DoesNotExist:
        return None

# Helper function to generate a string that represents the current weekday
def _current_week():
	today = date.today()
	this_monday = today - timedelta(days=today.weekday())
	this_sunday = this_monday + timedelta(days=6)
	return 'Week of {0} {1} to {2} {3}'.format(this_monday.strftime('%B'), this_monday.strftime('%d').lstrip('0'), this_sunday.strftime('%B'), this_sunday.strftime('%d').lstrip('0'))