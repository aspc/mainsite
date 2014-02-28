# Scraper for HMC (Hoch-Shanahan) dining hall.

import requests
from bs4 import BeautifulSoup

class MuddBackend(object):
    def __init__(self):
        self.DAYS = ['friday', 'saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday']

    def _get_menu_data(self, week_number):
        resp = requests.get('http://hmcdining.com/Week%d.htm' % week_number)
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

        for day in self.DAYS:
            day_node = menu_data.find(id=day) # i.e. Find all the meals that correspond to 'monday' first

            day_elements = day_node.find_all('tr')

            for element in day_elements:
                if len(element.find_all('td', {'class':'mealname'})):
                    current_meal = element.find_all('td', {'class':'mealname'})[0].text.lower()
                    continue
                elif element.find('div', {'class':'menuitem'}) and element.find('div', {'class':'menuitem'}).find('span'):
                    try:
                        menus[day[:3].lower()][current_meal].append(element.find('div', {'class':'menuitem'}).find('span').text)
                    except KeyError: # Create the list if nothing has been loaded yet for this day's current meal
                        menus[day[:3].lower()][current_meal] = [element.find('div', {'class':'menuitem'}).find('span').text]

        return menus

    def menu(self):
        return self._parse_menu_data(self._get_menu_data(6))