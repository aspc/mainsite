# Scraper for Scripps (Malott) dining hall.

import requests
from datetime import datetime
from bs4 import BeautifulSoup

class ScrippsBackend(object):
	def __init__(self):
		self.DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

		# Note that the Scripps menu calendar starts on Monday, not Sunday
		self.menu_urls = [
			'https://scrippsdining.sodexomyway.com/Images/WeeklyMenu_tcm1567-47109.htm',
			'https://scrippsdining.sodexomyway.com/Images/WeeklyMenu_tcm1567-47105.htm',
			'https://scrippsdining.sodexomyway.com/Images/WeeklyMenu_tcm1567-47113.htm',
			'https://scrippsdining.sodexomyway.com/Images/WeeklyMenu_tcm1567-50861.htm',
			'https://scrippsdining.sodexomyway.com/Images/WeeklyMenu_tcm1567-51952.htm'
		]

	def _get_menu_data(self, week_number):
		menu_url = self.menu_urls[week_number]
		resp = requests.get(menu_url)
		if resp.status_code == 404: # Sometimes Mudd does not update its menu on time...
			return None
		else:
			return BeautifulSoup(resp.text)

	def _parse_menu_data(self, menu_data):
		current_meal = None

		# Menu structure to return
		menus = {
			'mon': {}, # Each day dict contains key value pairs as meal_name, [fooditems]
			'tue': {},
			'wed': {},
			'thu': {},
			'fri': {},
			'sat': {},
			'sun': {}
		}

		if not menu_data: # If the data can't be loaded for some reason, just return an empty dict
			return menus

		for day in self.DAYS:
			day_node = menu_data.find(id=day) # i.e. Find all the meals that correspond to 'monday' first

			day_elements = day_node.find_all('tr')

			for element in day_elements:
				if len(element.find_all('td', {'class':'mealname'})):
					current_meal = element.find_all('td', {'class':'mealname'})[0].text.lower()
					if (day == 'saturday' or day == 'sunday') and current_meal == 'lunch':
						current_meal = 'brunch'
					continue
				elif element.find('div', {'class':'menuitem'}) and element.find('div', {'class':'menuitem'}).find('span'):
					try:
						menus[day[:3].lower()][current_meal].append(element.find('div', {'class':'menuitem'}).find('span').text)
					except KeyError: # Create the list if nothing has been loaded yet for this day's current meal
						menus[day[:3].lower()][current_meal] = [element.find('div', {'class':'menuitem'}).find('span').text]

		return menus

	def menu(self):
		# Scripps stupidly changes the url to their menu every week (honestly, who conceived of this...?)
		# so we have to calculate the difference in weeks from now and the start of term
		# This code is fairly unstable and should be checked at the beginning of each semester at the very least
		start_date = datetime(year=2015, month=1, day=19)
		week_number = (datetime.today() - start_date).days / 7  # 0-indexed

		return self._parse_menu_data(self._get_menu_data(week_number))