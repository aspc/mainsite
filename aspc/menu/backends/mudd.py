import requests
import demjson
from bs4 import BeautifulSoup
import datetime
from dateutil import parser

class MuddBackend(object):
    def __init__(self):
        #self.menus format:
        # {'day':
        #    {'meal':
        #	    {'station':['fooditem']}
        #    }
        # }
        self.menus = {
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
        index_url = 'https://hmc.sodexomyway.com/dining-choices/index.html'
        resp = requests.get(index_url)
        doc = BeautifulSoup(resp.text, "html.parser")
        hours = doc.find_all('div', {'class': 'accordionBody'})[1]
        return hours.span

    def get_monday(self):
        """
        Return datetime object of Monday of week
        """
        week = []
        now = datetime.datetime.now().date()
        return now - datetime.timedelta(days=now.weekday()) #Monday

    def menu(self):
        """
        Returns menu for this week
        """
        index_url = 'https://hmc.sodexomyway.com/smgmenu/json/harvey%20mudd%20college%20-%20resident%20dining'
        raw_string = requests.get(index_url).text

        #The link above isn't a traditional json - it's a js file with:
        #1. a pseudo json (the keys aren't contained in strings and therefore can't
        #be processed by the traditional json library)
        #2. a data object contains all the information for a given food item

        #Isolate the pseudo json and make it more json-like
        parts  = raw_string.split("aData=new Object();")
        json_part = parts[0].split("menuData = ")
        json_string = "{ menuData : " + json_part[1].strip()[0:-1] + " }"
        #Run it through demjson, which can handle the weird format
        json_obj = demjson.decode(json_string)
        #Sometimes, the json will have 2+ weeks' menus in it. Check which one
        #matches the current week.
        #If the check doesn't work, display whatever week it has available...
        menu_json = json_obj['menuData'][0]['menus'][0]['tabs']
        for i in range(len(json_obj['menuData'])):
            start_date = json_obj['menuData'][i]['startDate']
            if parser.parse(start_date).date() == self.get_monday():
                menu_json = json_obj['menuData'][i]['menus'][0]['tabs']
        #Parse contents of 'aData'
        aData = parts[1]
        fooditem_dict = {}
        for entry in aData.split("\r\n"):
            entry_parts = entry.split("]=new Array(") #looks like ["aData['###'","'# oz, '0'..."]
            if len(entry_parts)==2:
                fooditem_id = entry_parts[0].split("aData[")[1][1:-1] #remove surrounding ''s
                fooditem_data = entry_parts[1][:-1] #remove ) at end
                fooditem_data_list = [data[1:-1] for data in fooditem_data.split(",")]
                fooditem_dict[fooditem_id]=fooditem_data_list

        for day in menu_json:
            day_dict = {} # key: meal_name -> value: (key: station -> value: [items])
            day_name = day["title"].lower()[:3] #Monday -> mon
            for meal in day["groups"]:
                meal_name = meal["title"].lower()
                if (day_name == "sat" or day_name == "sun") and meal_name == "lunch":
                    meal_name = "brunch"
                day_dict[meal_name] = {} #station->[food items]
                station_list = meal['category']
                for station in station_list:
                    station_name = station['title']
                    food_id_list = station['products']
                    for food_id in food_id_list:
                        food_name = fooditem_dict[food_id][22].replace("\\","") #'General Tso\'s Tofu' -> 'General Tso's Tofu'
                        if station_name not in day_dict[meal_name].keys():
                            day_dict[meal_name][station_name] = [food_name]
                        else:
                            day_dict[meal_name][station_name].append(food_name)
            self.menus[day_name] = day_dict
        return self.menus
