# Scraper for CMC (Collins) dining hall.
#
# Originally from https://github.com/sean-adler/5c-dining-api

import feedparser
from bs4 import BeautifulSoup
from collections import defaultdict

class CmcBackend(object):
    rss = feedparser.parse('http://legacy.cafebonappetit.com/rss/menu/50')

    day_range = range(7)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    def _dayDict(self, day_index):
        entry = BeautifulSoup(self.rss.entries[day_index].summary)
        date = self.rss.entries[day_index].title[:4]
        tm = titles_and_meals = entry.findAll(['h3', 'h4'])

        meal_dict = defaultdict(list)

        for m in tm:
            if m.name == 'h3':
                meal_title = m.text
            elif m.name == 'h4':
                food = m.text.strip().split(', ')
                for f in food:
                    station_and_food = f.split('] ')
                    if len(station_and_food) > 1:
                        station = station_and_food[0]
                        food = station_and_food[1]
                        meal_dict[meal_title].append(food)
                    else:
                        food = station_and_food[0]
                        meal_dict[meal_title].append(food)

        meal_dict = dict(meal_dict)
        return {key.lower(): value for key,value in meal_dict.iteritems()}

    def menu(self):
        return {self.days[i][:3] : self._dayDict(i) for i in self.day_range}