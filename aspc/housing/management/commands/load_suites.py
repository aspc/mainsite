from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import transaction
from aspc.college.models import Building, Floor
from aspc.housing.models import Room, Suite
import csv

class Command(BaseCommand):
    args = '[filename]'
    help = 'loads/updates suite records, optionally from a csv file\n' \
           'of the format [building shortname],[space separated room numbers]'
    
    def import_suite(self, row):
        try:
            bldg = Building.objects.get(shortname=row[0])
        except Building.DoesNotExist:
            raise CommandError('Suite references building {0} that doesn\'t exist'.format(row[0]))
        
        occupancy = int(row[1])
        
        room_nums = row[2].split(' ')
        
        check_exists = Room.objects.filter(floor__building=bldg, number__in=room_nums)
        if check_exists.count() != len(room_nums):
            raise CommandError('Suite [{0}] references rooms that don\'t all exist (got {1} instead of {2})'.format([room_nums, check_exists.count(), len(room_nums)]))
        
        Room.objects.suite_from_rooms(check_exists, occupancy)
            
    @transaction.commit_manually
    def handle(self, *args, **options):
        if len(args) > 0:
           fpath = args[0]
        else:
           fpath = settings.DATA_PATHS['housing']['suites']

        try:
           fh = open(fpath, 'r')
        except:
           raise CommandError('Could not open file "{0}" for reading'.format(fpath))

        fh.readline() # skip heading row
        csvreader = csv.reader(fh)
        
        try:
            Suite.objects.all().delete()
            for row in csvreader:
               self.import_suite(row)
        except:
            transaction.rollback()
            raise
        else:
            transaction.commit()