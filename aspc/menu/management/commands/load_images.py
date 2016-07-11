from django.core.management.base import BaseCommand
from aspc.menu.models import Menu, Item
import grequests, json
# from aspc.settings import GOOGLE_SEARCH_KEY, GOOGLE_SEARCH_CX
from aspc.settings import BING_SEARCH_KEY
from urllib import urlencode


class Command(BaseCommand):
	args = ''
	help = 'loads the images of food items'

	def handle(self, *args, **options):
		if len(args):
			self.stdout.write('loadmenu takes no arguments \n')
			return
        items = Item.objects.all()

        def split_into_chunks(l, n=50):
            return [l[i:i+n] for i in xrange(0, len(l), n)]

        def process_items(items):
            # GOOGLE_SEARCH_URL = 'https://www.googleapis.com/customsearch/v1?'
            BING_SEARCH_URL = 'https://api.datamarket.azure.com/Bing/Search/v1/Image?$format=json&'
            unsent_requests, updated_items = [], []
            for item in items:
                if not item.image_url:
                    # params = {'q': item.name, 'key': GOOGLE_SEARCH_KEY, 'cx':GOOGLE_SEARCH_CX, 'num':1, 'searchType': "image"}
                    params = {'Query':"'"+item.name.encode('utf-8')+"'"}
                    # unsent_requests.append(grequests.get(url=GOOGLE_SEARCH_URL,  params=params))
                    unsent_requests.append(grequests.get(url=BING_SEARCH_URL+urlencode(params),
                                                         auth=(BING_SEARCH_KEY,BING_SEARCH_KEY)))
                    updated_items.append(item)
            responses = grequests.map(unsent_requests)
            item_response_pairs = list(zip(updated_items, responses))
            for item, resp in item_response_pairs:
                data = json.loads(resp.text)
                print(data)
                try:
                    # link = data['items'][0]['link']
                    link = data['d']['results'][0]['Thumbnail']['MediaUrl']
                except Exception as e:
                    link = ''
                item.image_url = link
                item.save()
                print(item.name+" : "+item.image_url)

        items_chunks = split_into_chunks(items)
        for chunk in items_chunks:
            process_items(chunk)

