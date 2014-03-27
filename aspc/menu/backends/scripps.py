# Scraper for Scripps (Malott) Dining Hall
#
# Originally from https://github.com/sean-adler/5c-dining-api

import feedparser

class ScrippsBackend(object):
    DATA = feedparser.parse('https://emsweb.claremont.edu/ScrippsMC/RSSFeeds.aspx?data=3p3oPLk3vPIqlgR7GVicJVEY1uoLxMswNw0YQhkyHqT6cGpSHWhEe5k4c3Exs8yX')

    DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    WEEKDAYS = DAYS[:5]
    WEEKENDS = DAYS[5:]

    WEEKDAY_MEALS = ['breakfast', 'lunch', 'dinner']
    WEEKEND_MEALS = ['brunch', 'dinner']

    # Takes a day from the Scripps RSS feed and returns a dict representation.
    def _dayDict(self, day):
        day_meals = {entry['title'].lower(): self._formatMeals(entry['summary_detail']['value']) for entry in self.DATA['entries'] if day in entry['published']}

        if day in self.WEEKDAYS:
            for meal in self.WEEKDAY_MEALS:
                if meal not in day_meals: day_meals[meal] = []

        elif day in self.WEEKENDS:
            for meal in self.WEEKEND_MEALS:
                if meal not in day_meals: day_meals[meal] = []

        return day_meals

    # Takes a semicolon-delimited string of meals and returns a list of meals.
    def _formatMeals(self, meals):
        meals = filter(None, meals.split(';'))
        return map(lambda s: s.strip(), meals)

    def menu(self):
        return {day.lower() : self._dayDict(day) for day in self.DAYS}