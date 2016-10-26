# Scraper for HMC (Hoch-Shanahan) dining hall.

import requests
from bs4 import BeautifulSoup

class MuddBackend(object):
	def __init__(self):
		self.DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

	def _get_menu_url(self):
		index_url = 'https://hmc.sodexomyway.com/dining-choices/index.html'
		resp = requests.get(index_url)
		doc = BeautifulSoup(resp.text)
		menu_url = doc.find_all('div', {'class': 'accordionBody'})[0].find_all('a')[0]['href']
		return 'https://hmc.sodexomyway.com' + menu_url # The href attribute is not the full URL for some reason

	def _get_menu_data(self, menu_url):
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
		# Mudd stupidly changes the url to their menu every week (honestly, who conceived of this...?)
		# It used to happen in a standardized format (i.e. numerical progression), but now it appears to be quite random
		# So we instead have to first inspect the DOM of the dining hall "index page" for the weekly URL, and then scrape that!

		return self._parse_menu_data(self._get_menu_data(self._get_menu_url()))