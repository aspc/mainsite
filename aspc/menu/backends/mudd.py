# Scraper for HMC (Hoch-Shanahan) dining hall.

import requests
from datetime import datetime
from bs4 import BeautifulSoup

class MuddBackend(object):
    def __init__(self):
        self.DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    def _get_menu_data(self, week_number):
        # Note that the HMC menu calendar starts on Monday, not Sunday
        # The old URL used to be at least somewhat predicable, now it seems to change weekly on the whim of whoever updates the menu
        # Record of past URL patterns:
        # menu_url = 'http://hmcdining.com/Week%d.htm' % week_number
        # menu_url = 'http://www.hmcdining.com/Wk%dSpring.htm' % week_number
        # menu_url = 'http://www.hmcdining.com/dining/Wk%dSpringCycle2.htm' % week_number
        # menu_url = 'http://www.hmcdining.com/Wk%dSpringCycle2.htm' % week_number
        # menu_url = 'http://www.hmcdining.com/dining/Week%dF14.htm' % week_number
        # menu_url = 'http://www.hmcdining.com/dining/Week%dF14_2.htm' % week_number
        # menu_url = 'http://www.hmcdining.com/dining/Week%dF14_3.htm' % week_number
        # menu_url = 'https://hmc.sodexomyway.com/images/Week%20{wn}%20F14_3_tcm1300-2231.htm'.format(wn=week_number)
        # menu_url = 'https://hmc.sodexomyway.com/images/Week%204%20F14_3_tcm1300-41684.htm'
        # menu_url = 'https://hmc.sodexomyway.com/images/Week%201%20F14_4_tcm1300-42239.htm'
        # menu_url = 'https://hmc.sodexomyway.com/images/Week%201%20F14_4%20v2_tcm1300-42239.htm'
        # menu_url = 'https://hmc.sodexomyway.com/images/Week%201%20S15_tcm1300-46421.htm'
        menu_url = 'https://hmc.sodexomyway.com/images/Week%202%20S15_tcm1300-47713.htm'
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
        # HMC stupidly changes the url to their menu every week (honestly, who conceived of this...?)
        # so we have to calculate the difference in weeks from now and the start of term
        # This code is fairly unstable and should be checked at the beginning of each semester at the very least
        start_date = datetime(year=2014, month=11, day=3)
        week_number = (datetime.today() - start_date).days / 7 + 1

        return self._parse_menu_data(self._get_menu_data(week_number))