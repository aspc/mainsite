from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from aspc.college.models import Building, Floor
from aspc.housing.models import Room
import csv

class Command(BaseCommand):
    args = '[filename]'
    help = 'loads/updates room records, optionally from a csv file\n' \
           'of the format shortname,name,floors,lat,long'
    
    def import_room(self, room):
        try:
            bldg = Building.objects.get(shortname=room[0])
        except Building.DoesNotExist:
            raise CommandError('Room references building {0} that doesn\'t exist'.format(room[0]))
        
        try:
            floor = Floor.objects.get(building=bldg, number=room[1])        
        except Floor.DoesNotExist:
            raise CommandError('Room references floor {0} of {1} that doesn\'t exist [{2}]'.format(room[1], bldg, room))
        except:
            raise Exception('funny business with {0}'.format(room))
        
        try:
            room_instance = Room.objects.get(floor=floor, number=room[2])
        except Room.DoesNotExist:
            room_instance = Room(floor=floor, number=room[2])
            room_instance.save()
        
        if len(room) >= 4:
            room_instance.size = float(room[3]) if room[3] not in ['', None, 'None'] else None
        
        if len(room) >= 5:
            room_instance.occupancy = Room.OCCUPANCY_LOOKUP[room[4]]
        
        room_instance.save()
            
    
    def handle(self, *args, **options):
        if len(args) > 0:
            fpath = args[0]
        else:
            fpath = settings.DATA_PATHS['housing']['rooms']
        
        try:
            fh = open(fpath, 'r')
        except:
            raise CommandError('Could not open file "{0}" for reading'.format(fpath))
        
        fh.readline() # skip heading row
        csvreader = csv.reader(fh)
        
        for row in csvreader:
            self.import_room(row)
