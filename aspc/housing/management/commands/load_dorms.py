from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from aspc.college.models import Building, Floor
import csv

class Command(BaseCommand):
    args = '[filename]'
    help = 'loads/updates building records, optionally from a csv file\n' \
           'of the format shortname,name,floors,lat,long'
    
    def import_building(self, bldg):
        print bldg
        try:
            b = Building.objects.get(shortname=bldg[0])
        except Building.DoesNotExist:
            b = Building(shortname=bldg[0])
        if len(bldg) == 5: # lat and long provided
            b.latitude = bldg[3]
            b.longitude = bldg[4]
        b.name = bldg[1]
        b.type = Building.TYPES_LOOKUP['Dormitory']
        b.save()
        
        floors = [int(a) for a in bldg[2].split(' ')] # numeric list from space delimited
        for f in floors:
            try:
                Floor.objects.get(building=b, number=f)
            except Floor.DoesNotExist:
                new_floor = Floor(building=b, number=f)
                new_floor.save()
    
    def handle(self, *args, **options):
        if len(args) > 0:
            fpath = args[0]
        else:
            fpath = settings.DATA_PATHS['housing']['buildings']
        
        try:
            fh = open(fpath, 'r')
        except:
            raise CommandError('Could not open file "{0}" for reading'.format(fpath))
        
        fh.readline() # skip heading row
        csvreader = csv.reader(fh)
        
        for row in csvreader:
            self.import_building(row)