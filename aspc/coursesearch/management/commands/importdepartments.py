from django.core.management.base import BaseCommand, CommandError
import django.db.utils
from aspc.coursesearch.models import Department

class Command(BaseCommand):
    args = ''
    help = 'imports departments from data/scraped_departments.py'

    def handle(self, *args, **options):
        from aspc.data.scraped_departments import departments
        for code, name in departments:
            self.stdout.write('trying "%s"... ' % code)
            name = name.replace('&amp;', '&')
            newdept = Department(code=code, name=name)
            try:
                newdept.save()
                self.stdout.write('Successfully added "%s"\n' % code)
            except django.db.utils.IntegrityError:
                self.stdout.write('exists, skipping\n')