from django.core.management.base import BaseCommand
from aspc.events.models import EventController, FacebookEventPageController

class Command(BaseCommand):
    args = ''
    help = 'scrapes new events from collegiatelink and gathers new events from submitted Facebook pages that are being watched'

    def handle(self, *args, **options):
        if len(args):
            self.stdout.write('refreshevents takes no arguments \n')
            return

        # Gather new collegiatelink events
        EventController().fetch_collegiatelink_events();
        self.stdout.write('gathered collegiatelink events \n')

        # Gather new Facebook events from watched pages
        facebook_event_pages = FacebookEventPageController().facebook_event_pages()
        for event_page in facebook_event_pages:
            FacebookEventPageController().scrape_page_events(event_page)
        self.stdout.write('gathered Facebook page events \n')