# Scraper for Pitzer (McConnell) dining hall.
#
# Originally from https://github.com/sean-adler/5c-dining-api

import feedparser
from collections import defaultdict
from bs4 import BeautifulSoup

class PitzerBackend(object):
    rss = feedparser.parse('http://legacy.cafebonappetit.com/rss/menu/219')
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    menus = { # Menu structure to return
        'mon': {}, # Each day dict contains key value pairs as meal_name, [fooditems]
        'tue': {},
        'wed': {},
        'thu': {},
        'fri': {},
        'sat': {},
        'sun': {}
    }

    def menu(self):
        # for everything on the site
        for entry in self.rss.entries:
            body = BeautifulSoup(entry.summary)
            date = entry.title[:4]
            # everything that has a h3 or h4 tag
            tm = titles_and_meals = body.findAll(['h3', 'h4'])

            meal_dict = defaultdict(list)
            # print("meal dict first: ", meal_dict)

            toAdd = ""
            add_save = ""
            to_save = ""
            old_list = []

            # take all of the meals and foods
            for m in tm:
                # num = -1
                if m.name == 'h3':                  # is a meal
                    meal_title = m.text
                elif m.name == 'h4':                # is a food item
                    food = m.text.strip().split(', ')
                    for f in food:
                        station_and_food = f.split('] ')
                        if len(station_and_food) > 1:
                            station = station_and_food[0]
                            toAdd = station.title() [1:] #+ ":"
                            # because all breakfast meal lines are named "Breakfast"
                            if toAdd == "Breakfast":
                                toAdd = ""
                            # don't want repetition 
                            if toAdd not in meal_dict[meal_title]:
                                # meal_dict[meal_title][num + 1].append(toAdd)
                                # num += 1

                                my_dict = meal_dict[meal_title] = {}


                                my_list = meal_dict[meal_title][toAdd] = [] #defaultdict(list)


                            food = station_and_food[1]
                            my_list.append(food.title())

                            # testing for getting full inner dictionaries 
                            # have completed one thing, moving on to next
                            if (toAdd != add_save):
                                print ("adding here ", add_save, " ", to_save)
                                # meal_dict[to_save]
                            
                            old_list = my_list
                            to_save = my_dict           # the old, complete dictionary 
                            add_save = toAdd            # the old name of the stocks
                            # print("adding here ", f, " ", my_dict)
                        else:
                            food = station_and_food[0]
                            my_list.append(food.title())
                # print("LOOK Here ", meal_dict[meal_title][0])        

            # print ("meal dict second: ", meal_dict)
            meal_dict = dict(meal_dict)
            # print("md third: ", meal_dict)
            # meal_dict[0].append("I'm working?")

            # change back to iteritems for 2.7 - but runs on computer with items (3.5)
            self.menus[entry.title[:3].lower()] = {key.lower(): value for key, value in meal_dict.iteritems()}
        return (self.menus)
