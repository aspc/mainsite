import requests
import demjson
import datetime
import string
from dateutil import parser
from bs4 import BeautifulSoup


class CmcBackend(object):

    #self.menus format:
    # {'day':
    #    'meal': 
    #       'station':['fooditem']
    # }    
    menus = {
        'mon': {}, 
        'tue': {},
        'wed': {},
        'thu': {},
        'fri': {},
        'sat': {},
        'sun': {}
    }

    def get_hours(self):
        """
        returns hours of operation
        """
        index_url = 'http://collins-cmc.cafebonappetit.com/cafe/collins/'
        resp = requests.get(index_url)
        doc = BeautifulSoup(resp.text, "html.parser")
        hours = doc.find_all('div', {'class': 'cafe-details six columns end'})[0]
        return hours.text  

    def get_week(self):
        """
        Return string listing dates of current full week
        """
        week = []
        now = datetime.datetime.now().date()
        one_day = datetime.timedelta(days=1)
        sunday = now - datetime.timedelta(days=now.weekday())
        date = sunday
        for n in range(7):
            week.append(date.isoformat())
            date += one_day
        return ",".join(week)

    def menu(self):
        """
        Returns menu for this week
        """
        index_url = 'http://legacy.cafebonappetit.com/api/2/menus?format=json&cafe=50&date=%s'%(
        self.get_week())
        raw_string = requests.get(index_url).text
        
        menu_json= demjson.decode(raw_string)
        fooditem_dict = menu_json["items"] #use this to translate food item number id's into English
        
        for day in menu_json["days"]:
            day_dict = {} # key: meal_name -> value: (key: station -> value: [items])
            day_name = parser.parse(day["date"]).strftime("%A").lower()[:3] #Monday -> mon
            all_meals = day["cafes"]["50"]["dayparts"][0]
            for meal in all_meals:
                meal_name = meal["label"].lower()
                day_dict[meal_name] = {} #station->[food items]
                station_list = meal['stations']
                for station in station_list:
                    station_name = string.capwords(station['label'])
                    food_id_list = station['items']
                    for food_id in food_id_list:
                        food_name = string.capwords(fooditem_dict[food_id]["label"])
                        if fooditem_dict[food_id]["tier"] == 1: #tiers 2+ display too much detail
                            if station_name not in day_dict[meal_name].keys():
                                day_dict[meal_name][station_name] = [food_name]
                            else:
                                day_dict[meal_name][station_name].append(food_name)
            self.menus[day_name] = day_dict
        return self.menus