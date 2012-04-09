import logging
import pyodbc
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from aspc.coursesearch.tasks import update_catalog as update_task

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    args = ''
    help = """Performs a full schedule refresh with course data 
           from the JICSWS server provided by ITS"""

    def handle(self, *args, **options):
        update_task()