from django.core.management.base import BaseCommand
import re
import simplejson, urllib
from aspc.courses.models import Term


TERMS_URL = 'http://staging.aspc.pomona.edu/jicsws/terms'

class Command(BaseCommand):
    args = ''
    help = 'imports terms'

    def handle(self, *args, **options):
        terms = simplejson.load(urllib.urlopen(TERMS_URL))
        for term in terms:
            key = term['Key']
            try:
                obj = Term.objects.get(key=key)
                self.stdout.write('found existing for key: "%s"\n' % obj.code)
            except Term.DoesNotExist:
                obj = Term(key=key)
                self.stdout.write('adding new for key: "%s"\n' % obj.code)

            obj.year = term['Year']
            obj.session = term['Session']
            obj.subsession = term['SubSession']

            obj.save()

            self.stdout.write('Successfully added term "%s"\n' % obj.encode('utf-8'))
