from django.core.management.base import BaseCommand
from django.conf import settings
from aspc.courses.models import Term, Section
from aspc.courses.management.commands.import_courses import get_all_terms
import simplejson, urllib, re

ENROLLMENTS_URL = settings.COURSE_API_URL + 'courses/%s'


class Command(BaseCommand):
    args = ''
    help = 'refreshes course enrollment data'

    def handle(self, *args, **options):
        term = Term.objects.all().values_list('key', flat=True)[0]
        terms = get_all_terms(term)

        for t in terms:
            courses = simplejson.load(urllib.urlopen(ENROLLMENTS_URL % t))

            for course in courses:
                code = course['CourseCode']
                try:
                    object = Section.objects.get(code=code)
                    object.perms = course['PermCount']
                    if object.perms: int(object.perms)

                    object.spots = int(course['SeatsTotal'])
                    object.filled = int(course['SeatsFilled'])

                    object.save()

                    self.stdout.write('enrollments for section "%s" refreshed\n' % object.code)

                except Section.DoesNotExist:
                    self.stdout.write('skipping unknown section "%s"\n' % code)
