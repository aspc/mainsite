from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from aspc.housing.models import Room

class Command(BaseCommand):
    args = '[filename]'
    help = 'loads/updates room records, optionally from a csv file\n' \
           'of the format building_shortname,floor,number,size,occupancy,lat,long'
    
    def format_room(self, room):
        return ','.join([room.floor.building.shortname, unicode(room.floor.number), room.number, unicode(room.size) if room.size else u'', room.get_occupancy_display(), u"{0:.15f}".format(room.latitude) if room.latitude else u'', u"{0:.15f}".format(room.longitude) if room.longitude else u''])
    
    def handle(self, *args, **options):
        print 'building_shortname,floor,number,size,occupancy,lat,long'
        print '\n'.join([self.format_room(room) for room in Room.objects.all()])