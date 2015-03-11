from django.core.management.base import BaseCommand
from aspc.menu.models import Menu
from aspc.menu.backends.cmc import CmcBackend
from aspc.menu.backends.pitzer import PitzerBackend
from aspc.menu.backends.mudd import MuddBackend
from aspc.menu.backends.scripps import ScrippsBackend
from aspc.menu.backends.pomona import PomonaBackend
import json
import traceback

class Command(BaseCommand):
	args = ''
	help = 'loads the current week\'s menus from all seven dining halls'

	def handle(self, *args, **options):
		if len(args):
			self.stdout.write('loadmenu takes no arguments \n')
			return

		# Clear the previous week's meals
		Menu.objects.all().delete()

		# Scrape each menu source
		# All backends return data in the same format:
		# {'day':
		#   'meal': ['fooditem']
		# }

		try:
			cmc_meals = CmcBackend().menu()
			for day in cmc_meals:
				for meal in cmc_meals[day]:
					new_menu = Menu(dining_hall='cmc', day=day, meal=meal, food_items=json.dumps(cmc_meals[day][meal]))
					new_menu.save()
		except Exception as e:
			self.stdout.write('*ERROR* - loading cmc menus:\n %s \n' % traceback.format_exc())
		else:
			self.stdout.write('SUCCESS - cmc menus loaded \n')

		try:
			pitzer_meals = PitzerBackend().menu()
			for day in pitzer_meals:
				for meal in pitzer_meals[day]:
					new_menu = Menu(dining_hall='pitzer', day=day, meal=meal, food_items=json.dumps(pitzer_meals[day][meal]))
					new_menu.save()
		except Exception as e:
			self.stdout.write('*ERROR* - loading pitzer menus:\n %s \n' % traceback.format_exc())
		else:
			self.stdout.write('SUCCESS - pitzer menus loaded \n')

		try:
			mudd_meals = MuddBackend().menu()
			for day in mudd_meals:
				for meal in mudd_meals[day]:
					new_menu = Menu(dining_hall='mudd', day=day, meal=meal, food_items=json.dumps(mudd_meals[day][meal]))
					new_menu.save()
		except Exception as e:
			self.stdout.write('*ERROR* - loading mudd menus:\n %s \n' % traceback.format_exc())
		else:
			self.stdout.write('SUCCESS - mudd menus loaded \n')

		try:
			frary_meals = PomonaBackend().frary_menu()
			for day in frary_meals:
				for meal in frary_meals[day]:
					new_menu = Menu(dining_hall='frary', day=day, meal=meal, food_items=json.dumps(frary_meals[day][meal]))
					new_menu.save()
		except Exception as e:
			self.stdout.write('*ERROR* - loading frary menus:\n %s \n' % traceback.format_exc())
		else:
			self.stdout.write('SUCCESS - frary menus loaded \n')

		try:
			frank_meals = PomonaBackend().frank_menu()
			for day in frank_meals:
				for meal in frank_meals[day]:
					new_menu = Menu(dining_hall='frank', day=day, meal=meal, food_items=json.dumps(frank_meals[day][meal]))
					new_menu.save()
		except Exception as e:
			self.stdout.write('*ERROR* - loading frank menus:\n %s \n' % traceback.format_exc())
		else:
			self.stdout.write('SUCCESS - frank menus loaded \n')

		try:
			oldenborg_meals = PomonaBackend().oldenborg_menu()
			for day in oldenborg_meals:
				for meal in oldenborg_meals[day]:
					new_menu = Menu(dining_hall='oldenborg', day=day, meal=meal, food_items=json.dumps(oldenborg_meals[day][meal]))
					new_menu.save()
		except Exception as e:
			self.stdout.write('*ERROR* - loading oldenborg menus:\n %s \n' % traceback.format_exc())
		else:
			self.stdout.write('SUCCESS - oldenborg menus loaded \n')

		try:
			scripps_meals = ScrippsBackend().menu()
			for day in scripps_meals:
				for meal in scripps_meals[day]:
					new_menu = Menu(dining_hall='scripps', day=day, meal=meal, food_items=json.dumps(scripps_meals[day][meal]))
					new_menu.save()
		except Exception as e:
			self.stdout.write('*ERROR* - loading scripps menus:\n %s \n' % traceback.format_exc())
		else:
			self.stdout.write('SUCCESS - scripps menus loaded \n')