import dateutil.parser
from django.conf import settings
import requests
import urlparse
from aspc.events.backends import InvalidEventException
import re
import logging
import pytz

logger = logging.getLogger(__name__)

class FacebookBackend(object):
    required_fields = ('name', 'location', 'start_time', 'description')
    EVENT_LINK_TEMPLATE = 'https://graph.facebook.com/'
    accepts_link = re.compile(r'https?://(?:www\.)?facebook.com/events/(?P<resource_id>\d+)')

    def __init__(self, options=None):
        self.facebook_token = self._get_access_token()

    def _get_access_token(self):
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

        if response.status_code == 400:
            InvalidEventException("Unable to retrieve event details. Is the event public?")
        elif not response.status_code == 200:
            response.raise_for_status()

        return response.json()

    def get_event_data(self, event_url):
        event_id = self.accepts_link.match(event_url).groupdict()['resource_id']
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
            'host': event_data['owner']['name'],
            'url': 'http://www.facebook.com/events/' + event_id
        }

        if 'end_time' in event_data.keys():
            end_dt = dateutil.parser.parse(event_data['end_time'])
            normalized['end'] = end_dt.astimezone(pytz.UTC)

        return normalized