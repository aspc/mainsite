from django.core.management.base import BaseCommand
from django.contrib.webdesign import lorem_ipsum
from aspc.events.models import Event
import datetime
import random

class Command(BaseCommand):
    args = '<events per day>'
    help = 'generates some fake events'
    
    _locations = (
        'Doms Lounge',
        'SCC 207',
        'Seaver Theatre',
        'Big Bridges',
        'Pomona College Museum of Art',
    )
    
    _hosts = (
        'Pomona Events Committee',
        'Cheese Club',
        'Alumni Office',
        'Career Development Office',
        'Bottom Line Theatre',
    )
    
    _adjectives = (
        'Awesome',
        'New',
        'Weekly',
        'Annual',
        'Inaugural',
        'Substance-free',
    )
    
    _nouns = (
        'Table Manners',
        'Kitten',
        'Physics & Astronomy',
        'Live Music',
        'Digital',
    )
    
    _types = (
        'Exhibition',
        'Performance',
        'Reception',
        'Lecture',
        'Party',
        'Dance',
        'Celebration',
    )

    def handle(self, *args, **options):
        if len(args):
            num_events = int(args[0])
        else:
            num_events = 10
        
        self.stdout.write('Generating %i fake events for the next 5 days\n' % (num_events,))
        today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        for day in range(6):
            for evtnum in range(num_events):
                new_event = Event()
                new_event.name = "{adj} {noun} {type}".format(
                    adj=random.choice(self._adjectives),
                    noun=random.choice(self._nouns),
                    type=random.choice(self._types)
                )
                
                new_event.start = today + datetime.timedelta(days=day, hours=8 + evtnum)
                new_event.end = new_event.start + datetime.timedelta(minutes=30)
                new_event.location = random.choice(self._locations)
                new_event.description = lorem_ipsum.paragraph()
                new_event.host = random.choice(self._hosts)
                new_event.url = "http://aspc.pomona.edu/"
                new_event.status = 'approved'
                
                new_event.save()
                self.stdout.write("Saved event '%s'" % (new_event.name,))
        