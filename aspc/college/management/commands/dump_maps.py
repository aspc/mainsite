from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.conf import settings
from django.db import transaction
from aspc.college.models import Building, Floor, Map
import csv, os.path

class Command(BaseCommand):
    args = ''
    help = 'outputs a maps data file in the format used by load_maps'
    
    def handle(self, *args, **options):
        a = Map.objects.all()
        # TODO ugly one liner.. :\
        print 'building,floor,ne,sw'
        print '\n'.join([','.join((k.floor.building.shortname, unicode(k.floor.number), ';'.join((unicode(k.n), unicode(k.e))), ';'.join((unicode(k.s), unicode(k.w))))) for k in a])
