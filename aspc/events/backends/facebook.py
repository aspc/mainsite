import dateutil.parser
from django.conf import settings
import requests
import urlparse
from glean.backends import InvalidEventException
from aspc.events.models import Event
import re
import logging
import pytz

logger = logging.getLogger(__name__)

class FacebookBackend(object):
    required_fields = ('name', 'location', 'start_time', 'description')
    EVENT_LINK_TEMPLATE = 'https://facebook.com/events/'
    accepts_link = re.compile(r'https?://(?:www\.)?facebook.com/events/(?P<resource_id>\d+)')

    def __init__(self, options=None):
        self.facebook_token = self._get_access_token()
        logger.debug("facebook_token = {0}".format(self.facebook_token))

    def _get_access_token():
        response = requests.get(
            'https://graph.facebook.com/oauth/access_token',
            params = {
                'client_id': settings.FACEBOOK_APP_ID,
                'client_secret': settings.FACEBOOK_APP_SECRET,
                'grant_type': 'client_credentials'
            }
        )
        response_data = urlparse.parse_qs(response.text) # Parses the returned query string

        return response_data['access_token']

    def _event_lookup(self, event_id):
        response = requests.get(
            self.EVENT_LINK_TEMPLATE + event_id,
            params = {
                'access_token': self.facebook_token
            }
        )

        if response.status_code == 400 or 'error' in response.json.keys():
            InvalidEventException("Unable to retrieve event details. Is the event public?")
        elif not response.status_code == 200:
            response.raise_for_status()

        return response.json

    def _get_event_data(self, resource_id):
        event_id = self.accepts_link.match(resource_id).groupdict()['resource_id']
        event_data = self._event_lookup(event_id)

        # Checks if the event has a start and end time
        if event_data.get('is_date_only', True):
            raise InvalidEventException("Submitted events must have a time and date")

        # Checks if the event has all the other necessary fields
        if not all((key in event_data.keys()) for key in self.required_fields):
            raise InvalidEventException("Unable to retrieve event details. Is the event public?")

        start_dt = dateutil.parser.parse(event_data['start_time'])
        start = start_dt.astimezone(pytz.UTC)

        normalized = {
            'name': event_data['name'],
            'location': event_data['location'],
            'start': start,
            'description': event_data.get('description', ''),
        }

        if 'end_time' in event_data.keys():
            end_dt = dateutil.parser.parse(event_data['end_time'])
            normalized['end'] = end_dt.astimezone(pytz.UTC)

        return normalized

    def new_event(self, event_id, initial_data=None):
        event_data = self._get_event_data()

        event = Event()

        for key, value in event_data.items():
            setattr(event, key, value)

        # Creates a new Event model with the Facebook data
        event.save()

        return event