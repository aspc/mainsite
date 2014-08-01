from django.core.management.base import BaseCommand
from aspc.sagelist.models import BookSale
from django.contrib.auth.models import User
import requests

class Command(BaseCommand):
	gsheets_key = '0AlsIsbXOfMnkdFhpQWdmeXdMRl9jTnljaXVuOW5qekE'
	gsheets_url_template = 'https://spreadsheets.google.com/feeds/list/{0}/od6/public/values?alt=json'
	gsheet_columns = [
		'title',
		'author',
		'isbn',
		'edition',
		'price',
		'uid'
	]

	def handle(self, *args, **options):
		for listing in self._fetch_recoop_listings():
			if listing['gsx$publish']['$t'] == 'y':
				recoop_id = listing['gsx$uid']['$t']

				try:
					book_sale, is_new = BookSale.objects.get_or_create(
						is_recoop=True,
						recoop_id=recoop_id,
						defaults={
							'title': listing['gsx$title']['$t'],
							'authors': listing['gsx$author']['$t'],
							'isbn': listing['gsx$isbn']['$t'],
							'edition': listing['gsx$edition']['$t'],
							'condition': 2,
							'price': listing['gsx$price']['$t'],
							'seller': User.objects.get(username='sustainability@pomona.edu')
						}
					)

					if not is_new:
						for column in self.gsheet_columns:
							setattr(book_sale, column, listing['gsx$' + column]['$t'])

					book_sale.save()
				except Exception as e:
					self.stdout.write('Error saving #' + recoop_id + ': ' + str(e))

				if is_new:
					self.stdout.write('Saving #' + recoop_id + '...')
				else:
					self.stdout.write('Updating #' + recoop_id + '...')

	def _fetch_recoop_listings(self):
		return requests.get(self.gsheets_url_template.format(self.gsheets_key)).json()['feed']['entry']