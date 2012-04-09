import logging
import pyodbc
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from aspc.coursesearch.tasks import smart_update as update_task

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    args = ''
    help = """Performs a conditional update of the course schedule 
           depending on the refresh history and whether new data are
           available"""

    def handle(self, *args, **options):
        update_task()