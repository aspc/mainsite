from django.core.management.base import BaseCommand, CommandError
import django.db.utils
from aspc.coursesearch.models import RequirementArea, CAMPUSES

class Command(BaseCommand):
    args = ''
    help = 'imports requirement areas from data/scraped_requirement_areas.py'

    def handle(self, *args, **options):
        from aspc.data.scraped_requirement_areas import requirement_areas
        for code, name in requirement_areas:
            self.stdout.write('trying "%s"... ' % code)
            name = name.replace('&amp;', '&')
            ra_campus = CAMPUSES[int(code[0]) - 1][0] # first char of ra code is 1-indexed college id
            try:
                newra = RequirementArea.objects.get(code=code)
                self.stdout.write('exists, updating\n')
            except RequirementArea.DoesNotExist:
                self.stdout.write('adding')
                newra = RequirementArea(code=code)
            newra.name = name
            newra.campus = ra_campus
            newra.save()
            self.stdout.write('Successfully updated "%s"\n' % code)
