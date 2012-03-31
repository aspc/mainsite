import logging
from django.conf import settings
import pyodbc
from django.core.management.base import BaseCommand, CommandError
import django.db.utils
from aspc.coursesearch.models import RequirementArea, CAMPUSES

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    args = ''
    help = 'Imports course data from the JICSWS server provided by ITS'

    def handle(self, *args, **options):
        logger.info("Starting full catalog update")
        logger.info("Connecting to {0}".format(settings.COURSE_DATA_DB['HOST']))
        cursor = pyodbc.connect(
          driver="FreeTDS",
          server=settings.COURSE_DATA_DB['HOST'],
          database=settings.COURSE_DATA_DB['NAME'],
          uid=settings.COURSE_DATA_DB['USER'],
          pwd=settings.COURSE_DATA_DB['PASSWORD']
        )
        logger.info("Full catalog update finished")