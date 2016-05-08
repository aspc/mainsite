from django.core.management.base import BaseCommand
from aspc.menu.models import Menu, Item
import grequests, json
from aspc.settings import GOOGLE_SEARCH_KEY, GOOGLE_SEARCH_CX

class Command(BaseCommand):
	args = ''
	help = 'loads the images of food items'

	def handle(self, *args, **options):
		if len(args):
			self.stdout.write('loadmenu takes no arguments \n')
			return
        items = Item.objects.all()
        GOOGLE_SEARCH_URL = 'https://www.googleapis.com/customsearch/v1?'
        unsent_requests, updated_items = [], []
        for item in items:
            if not item.image_url:
                params = {'q': item.name, 'key': GOOGLE_SEARCH_KEY, 'cx':GOOGLE_SEARCH_CX, 'num':1, 'searchType': "image"}
                unsent_requests.append(grequests.get(url=GOOGLE_SEARCH_URL,  params=params))
                updated_items.append(item)
        responses = grequests.map(unsent_requests)
        item_response_pairs = list(zip(updated_items, responses))
        for item, resp in item_response_pairs:
            data = json.loads(resp.text)
            try:
                link = data['items'][0]['link']
            except Exception as e:
                link = ''
            item.image_url = link
            item.save()
            print(item.name+" : "+item.image_url)


