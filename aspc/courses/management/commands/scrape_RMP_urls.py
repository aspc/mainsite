from django.core.management.base import BaseCommand
from aspc.courses.models import Instructor, RMPInfo
from bs4 import BeautifulSoup as bs
import grequests
import urllib


class Command(BaseCommand):
    args = ''
    help = 'loads the images of food items'

    def handle(self, *args, **options):
        college_names = {'PO': 'Pomona',
                         'PZ': 'Pitzer',
                         'CMC': 'Claremont Mckenna',
                         'SC': 'Scripps',
                         'HM': 'Harvey Mudd',
                         'KS': 'Keck Science',
                         'CU': 'Claremont Graduate',
                         'CGU': 'Claremont Graduate',
                         'UU': ''}
        if len(args):
            self.stdout.write('scrape_RMP_urls takes no arguments \n')
            return
        instructors = [instructor for instructor in Instructor.objects.all() if not instructor.get_RMPInfo()]

        def split_into_chunks(l, n=25):
            return [l[i:i+n] for i in xrange(0, len(l), n)]

        def remove_middle_letter(name):
            if not '.' in name:
                return name
            ind = name.index('.')
            return name[:ind-1] + name[ind+1:]

        def get_links_for_instructors(instructors):
            urls = []
            for instructor in instructors:
                query = remove_middle_letter(instructor.name) + ' ' + college_names[instructor.get_campus()]
                arg = { 'query' : query}
                url = 'http://www.ratemyprofessors.com/search.jsp?'+urllib.urlencode(arg)
                urls.append(url)
            unsent_request = (grequests.get(url) for url in urls)
            results = grequests.map(unsent_request)
            for i, r in enumerate(results):
                soup = bs(r.text,'html.parser')
                listing = soup.find('li',{'class':'listing PROFESSOR'})
                if listing:
                    href = 'http://www.ratemyprofessors.com' + listing.find('a')['href']
                    rmp = RMPInfo(instructor=instructors[i], url=href)
                    rmp.save()
                    print 'Get RMP link for ' + instructors[i].name + ' : ' + href

        instructor_chunks = split_into_chunks(instructors)
        for chunk in instructor_chunks:
            get_links_for_instructors(chunk)
