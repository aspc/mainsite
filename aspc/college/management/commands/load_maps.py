from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.conf import settings
from django.db import transaction
from aspc.college.models import Building, Floor, Map
import csv, os.path

class Command(BaseCommand):
    args = '[filename]'
    help = 'loads/updates building records, optionally from a csv file\n' \
           'of the format shortname,name,floors,lat,long'

    def import_map(self, map_row):
        if not map_row:
            return
        try:
            b = Building.objects.get(shortname=map_row[0])
        except Building.DoesNotExist:
            raise CommandError('Map [{0}] references building {1} that does not exist'.format(map_row, map_row[0]))

        try:
            floor = Floor.objects.get(building=b, number=map_row[1])
        except Floor.DoesNotExist:
            raise CommandError('Map [{0}] references floor {1} that does not exist'.format(map_row, map_row[1]))

        try:
            map_instance = Map.objects.get(floor=floor)
        except Map.DoesNotExist:
            map_instance = Map(floor=floor)

        map_instance.n, map_instance.e = map_row[2].split(';')
        map_instance.s, map_instance.w = map_row[3].split(';')

        try:
            filename = "{0}_{1}.png".format(map_row[0], map_row[1])
            map_file = open(os.path.join(settings.DATA_PATHS['housing']['maps_dir'], filename), 'r')
        except IOError:
            raise CommandError("Map file doesn't exist (or couldn't be opened) for [{0}]".format(map_row))

        if map_instance.id:
            map_instance.image.delete()

        map_instance.image.save(filename, File(map_file))

        map_instance.save()
        print "Saved map instance ", map_instance

    @transaction.set_autocommit()
    def handle(self, *args, **options):
        if len(args) > 0:
            fpath = args[0]
        else:
            fpath = settings.DATA_PATHS['housing']['maps']

        try:
            fh = open(fpath, 'r')
        except:
            raise CommandError('Could not open file "{0}" for reading'.format(fpath))

        fh.readline() # skip heading row
        csvreader = csv.reader(fh)

        try:
            for row in csvreader:
               self.import_map(row)
        except:
            transaction.rollback()
            raise
        else:
            transaction.commit()