from django.core.management.base import BaseCommand
from aspc.courses.models import Instructor, RMPInfo
from bs4 import BeautifulSoup as bs
import grequests
import urllib


class Command(BaseCommand):
    args = ''
    help = 'Scrape professor ratings from ratemyprofessor.com'

    def handle(self, *args, **options):
        if len(args):
            self.stdout.write('scrape_RMP_reviews takes no arguments \n')
            return
        infos = RMPInfo.objects.all()

        def split_into_chunks(l, n=25):
            return [l[i:i+n] for i in xrange(0, len(l), n)]

        def get_ratings_for_instructors(infos):
            urls = [info.url for info in infos]
            unsent_request = (grequests.get(url) for url in urls)
            results = grequests.map(unsent_request)
            for i, r in enumerate(results):
                soup = bs(r.text,'html.parser')
                listing = soup.find('div',{'class':'grade'})
                if listing and listing.text:
                    try:
                        rating = float(listing.text)
                        infos[i].rating = rating
                        infos[i].save()
                        self.stdout.write('Get RMP rating for ' + infos[i].instructor.name + ' : ' + str(rating))
                    except Exception as e:
                        self.stdout.write('Error: %s\n' % e)

        info_chunks = split_into_chunks(infos)
        for chunk in info_chunks:
            get_ratings_for_instructors(chunk)