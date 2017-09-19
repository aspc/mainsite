# Scraper for Pomona (Frank, Frary) dining halls.

from codecs import open
from datetime import date
from datetime import timedelta
import json
import lxml.html
import os
import re
import requests
import datetime
from urllib import quote

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

# Oldenborg scrapping is a little different
is_oldenborg = False

class PomonaBackend(object):
	def __init__(self):
		global is_oldenborg
		is_oldenborg = False

	class GoogleWorksheet(object):
		def __init__(self, w):
			self.w = w

		def __repr__(self):
			return repr(self.w)

		def __getitem__(self, key):
			return self.w[key]

		def _parse_hyphenated_date(self, s):
			try:
				month, day, year = map(int, s.split("-"))
				return date(2000 + year, month, day)
			except ValueError:
				return datetime.datetime.today()

		def date(self):
			return self._parse_hyphenated_date(self.w['title']['$t'])

	class GoogleCell(object):
		def __init__(self, c):
			position = c['title']['$t']
			self.column = str(position[0])
			self.row = int(position[1:])
			value = c['content']['$t']
			value = re.sub(u'[\xa0\s]+', ' ', value)

			if is_oldenborg:
				self.value = value.strip().encode('utf-8') # Oldenborg cells contain one fooditem each
			else:
				self.value = value.strip().encode('utf-8').split(',') # Creates a list

		def __repr__(self):
			return "(%s, %i, %s)" % (self.column, self.row, self.value)

	class NotFoundException(Exception):
		pass

	def _I(self, x): return x

	def _download(self, (url, after)):
		return after(self._download_helper_maybe_cache(url))

	def _download_helper_maybe_cache(self, url):
		# if debugging, comment out this line to go faster!
		return requests.get(url).text

		cachename = os.path.join(
	        PROJECT_ROOT,
	        "cache",
	        "{0}.cache".format(quote(url, safe=''))
	    )
		try:
			with open(cachename) as f:
				return f.read()
		except:
			data = requests.get(url).text
			with open(cachename, "w", encoding="utf-8") as f:
				f.write(data)
			return data

	def _find_spreadsheet_id(self, data):
		doc = lxml.html.fromstring(data)
		spreadsheet_id = doc.xpath('//*[@data-google-spreadsheet-id]')
		assert len(spreadsheet_id) == 1
		return spreadsheet_id[0].get('data-google-spreadsheet-id')

	def _get_worksheets_for_key(self, key):
		def after(resp):
			worksheets_json = json.loads(resp)
			worksheets = worksheets_json['feed']['entry']
			return map(self.GoogleWorksheet, worksheets)

		worksheets_url_template = "https://spreadsheets.google.com/feeds/worksheets/{key}/public/basic?alt=json"
		worksheets_url = worksheets_url_template.format(key=key)

		return (worksheets_url, after)

	def _get_cells_feed(self, worksheet):
		def after(resp):
			cells = json.loads(resp)['feed']['entry']
			return map(self.GoogleCell, cells)

		links = worksheet['link']
		rel = "http://schemas.google.com/spreadsheets/2006#cellsfeed"
		cells_links = filter(lambda l: l['rel'] == rel, links)
		assert len(cells_links) == 1
		cells_url = cells_links[0]['href'] + "?alt=json"

		return (cells_url, after)

	def _most_recent_monday(self, d):
		return d - timedelta(days=d.weekday())

	def _find(self, cond, seq):
		try:
			return next(iter(filter(cond, seq)))
		except StopIteration:
			raise self.NotFoundException(cond, seq)

	def _parse_frank_frary_cells(self, cells):
		# Frank: https://docs.google.com/spreadsheet/pub?key=0AsnKhcsREmJpdGV5RG5JbXpQVElSb3dHNHN3QmVaTVE&output=html
		# Frary: https://docs.google.com/spreadsheet/pub?key=0AsnKhcsREmJpdDdnWm1nMkY0MHBvYkNOQVRPZkRHOUE&output=html
		#
		# Spreadsheet format
		#
		#    |   A  |   B       |    C    |  D     |  E     |
		#  1 |      |           |         |        |        |
		#  2 |  Day |Station    |Breakfast|Lunch   |Dinner  |
		#  3 |Monday|Mealname   |         |        |        |
		#  4 |      |Mainline   |fooditem |fooditem|fooditem|
		#  5 |      |Veg Station| ...
		#  ...
		#
		# Continues in similar format for days Monday - Sunday

		# Entries to ignore
		ignored_cells = ['Day', 'Station', 'Breakfast', 'Lunch', 'Dinner', 'Brunch']

		# Days
		days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
		weekdays = ['mon', 'tue', 'wed', 'thu', 'fri']
		weekends = ['sat', 'sun']

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

		current_day = None
		current_meal = None
		ignored_row = None

		# Each cell is a tuple in the format (ColumnLetter, RowNumber, Value)
		for cell in cells:
			# Some cells are empty
			if not cell.value[0]:
				continue

			# Frary stores unneeded information in the first row
			if cell.row == 1:
				continue

			# A row marked to be ignored means that it contains extraneous meal name information
			if cell.row == ignored_row:
				continue

			# No need to parse the content from these cells
			if cell.value[0] in ignored_cells:
				continue

			# No need to collect the meal name (as of now...)
			if cell.column == 'B':
				continue

			# On weekends, the D column is not used
			if cell.column == 'D' and current_day is weekends:
				continue

			if cell.value[0] in days:
				current_day = cell.value[0][:3].lower()
				ignored_row = cell.row
				continue

			# Cells in the C, D, and E columns contain meal types
			if cell.column == 'C' and current_day in weekdays:
				current_meal = 'breakfast'
			elif cell.column == 'C' and current_day in weekends:
				current_meal = 'brunch'
			elif cell.column == 'D' and current_day in weekdays:
				current_meal = 'lunch'
			elif cell.column == 'E':
				current_meal = 'dinner'

			# Anything else that is in a cell should be a food item that we want to append to the appropriate menu
			try:
				current_menu = menus[current_day][current_meal]
			except KeyError: # Create the list if nothing has been loaded yet for this day's current meal
				current_menu = menus[current_day][current_meal] = []

			for food_item in cell.value:
				current_menu.append(food_item)

		return menus

	def _parse_oldenborg_cells(self, cells):
		# Oldenborg: https://docs.google.com/spreadsheet/pub?key=0AsnKhcsREmJpdHJBSUY2Y3Yxc0pqY0QwR29qOHhZUXc&output=html
		# Spreadsheet format
		#
		#    |   A     |   B       |    C   |    D    |    E   |   F    |
		#  1 |Oldenborg|           |        |         |        |        |
		#  2 |Dish     |Monday     |Tuesday |Wednesday|Thursday|Friday  |
		#  3 |Meal Name|OLC Ukraine|Mexican |Italian  |Asian   |American|
		#  4 |Soups    |fooditem   |fooditem|fooditem |fooditem|fooditem|
		#  ...
		#

		# Menu structure to return
		menus = {
			'mon': {
				'lunch': []
			},
			'tue': {
				'lunch': []
			},
			'wed': {
				'lunch': []
			},
			'thu': {
				'lunch': []
			},
			'fri': {
				'lunch': []
			},
			'sat': {
				'lunch': []
			},
			'sun': {
				'lunch': []
			},
		}

		# Each cell is a tuple in the format (ColumnLetter, RowNumber, Value)
		for cell in cells:
			# Some cells are empty
			if not cell.value[0]:
				continue

			# Unneeded information in the first three rows
			if cell.row < 4:
				continue

			# Cells in the B, C, D, E, and F columns contain food items for each day
			if cell.column == 'B':
				menus['mon']['lunch'].append(cell.value)
			elif cell.column == 'C':
				menus['tue']['lunch'].append(cell.value)
			elif cell.column == 'D':
				menus['wed']['lunch'].append(cell.value)
			elif cell.column == 'E':
				menus['thu']['lunch'].append(cell.value)
			elif cell.column == 'F':
				menus['fri']['lunch'].append(cell.value)

		return menus

	def _get_menu(self, url):
		search_date = (datetime.datetime.today() + datetime.timedelta(hours=4)).date()

		html = self._download((url, self._I))
		spreadsheet_key = self._find_spreadsheet_id(html)
		worksheets = self._download(self._get_worksheets_for_key(spreadsheet_key))
		worksheet = self._find(lambda _: _.date() == self._most_recent_monday(search_date), worksheets)
		cells = self._download(self._get_cells_feed(worksheet))

		if is_oldenborg:
			return self._parse_oldenborg_cells(cells)
		else:
			return self._parse_frank_frary_cells(cells)

	def frary_menu(self):
		return self._get_menu('http://www.pomona.edu/administration/dining/menus/frary')

	def frank_menu(self):
		return self._get_menu('http://www.pomona.edu/administration/dining/menus/frank')

	def oldenborg_menu(self):
		global is_oldenborg
		is_oldenborg = True;
		return self._get_menu('http://www.pomona.edu/administration/dining/menus/oldenborg')