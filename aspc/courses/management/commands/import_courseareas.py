from django.core.management.base import BaseCommand
import simplejson, urllib
from aspc.courses.models import RequirementArea, Department


AREAS_URL = 'http://staging.aspc.pomona.edu/jicsws/courseareas'

class Command(BaseCommand):
    args = ''
    help = 'imports departments and requirement areas'

    def handle(self, *args, **options):
        areas = simplejson.load(urllib.urlopen(AREAS_URL))
        for area in areas:
            code = area['Code']
            description = area['Description']

            if code[0].isdigit():
                try:
                    obj = RequirementArea.objects.get(code=code)
                    self.stdout.write('found existing requirement area for code: "%s"\n' % obj.code)
                except RequirementArea.DoesNotExist:
                    obj = RequirementArea(code=code)
                    self.stdout.write('adding new requirement area for code: "%s"\n' % obj.code)

                obj.name = description
                obj.campus = code[0]

                obj.save()

            else:
                try:
                    obj = Department.objects.get(code=code)
                    self.stdout.write('found existing department for code: "%s"\n' % obj.code)
                except Department.DoesNotExist:
                    obj = Department(code=code)
                    self.stdout.write('adding new department for code: "%s"\n' % obj.code)

                obj.name = description

                obj.save()

            self.stdout.write('Successfully added course area "%s"\n' % unicode(obj))
