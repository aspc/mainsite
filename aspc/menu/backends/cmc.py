# Scraper for CMC (Collins) dining hall.
#
# Originally from https://github.com/sean-adler/5c-dining-api

import feedparser
from bs4 import BeautifulSoup
from collections import defaultdict


class CmcBackend(object):
    rss = feedparser.parse('http://legacy.cafebonappetit.com/rss/menu/50')

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

    def menu(self):
        # for everything on the site
        for entry in self.rss.entries: #one day with all meals
            body = BeautifulSoup(entry.summary)
            date = entry.title[:3].lower() # 'mon'
            tm = titles_and_meals = body.findAll(['h3', 'h4'])
            #meal dict's format: MealName: {Station1: [food1, food2...]},{Station2...}
            meal_dict = {}
            
            # take all of the meals and foods
            for m in tm:
                # is a meal
                if m.name == 'h3':                  
                    meal_title = m.text
                    if meal_title not in meal_dict:
                        meal_dict[meal_title] = {}
                # Is a food item. Looks like '[station] food name'
                elif m.name == 'h4': 
                    raw_food_data = m.text.strip().split(', ')
                    #Format of f: "[station] food name"
                    for f in raw_food_data: 
                        #s_and_f format: list ['[station','food name']
                        station_and_food = f.split('] ') 
                        if len(station_and_food) > 1:
                            station_raw_string = station_and_food[0] #'[station'
                            #remove the '[' in front of station name
                            station = station_raw_string.title() [1:] #+ ":"
                            # because all breakfast meal lines are named "Breakfast"
                            if station == "Breakfast":
                                station = ""
                            # don't want repetition
                            
                            food_item = station_and_food[1]
                            if station not in meal_dict[meal_title].keys():
                                meal_dict[meal_title][station] = [food_item.title()]
                            else:
                                meal_dict[meal_title][station].append(food_item.title()) 
            self.menus[date] = meal_dict
                
        return (self.menus)
