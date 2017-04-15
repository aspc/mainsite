import dateutil.parser
from django.conf import settings
import requests
import urlparse
from aspc.events.exceptions import InvalidEventException, InvalidFacebookEventPageException
import re
import logging
import pytz
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class FacebookBackend(object):
    event_required_fields = ('name', 'place', 'start_time', 'description', 'owner')
    page_required_fields = ('name', 'link', 'id')
    GRAPH_API_TEMPLATE = 'https://graph.facebook.com/v2.8/'
    EVENT_LINK_TEMPLATE = re.compile(r'(?:https?:\/\/(?:www\.)?)?facebook.com/events/(?P<event_id>\d+)')

    def __init__(self, options=None):
        self.facebook_token = self._get_access_token()

    def _get_access_token(self):
        response = requests.get(
            self.GRAPH_API_TEMPLATE + 'oauth/access_token',
            params = {
                'client_id': settings.FACEBOOK_APP_ID,
                'client_secret': settings.FACEBOOK_APP_SECRET,
                'grant_type': 'client_credentials'
            }
        )
        response_data = json.loads(response.text) # Parses the returned query string

        #response_data = response.text
        return response_data['access_token']

    def _event_lookup(self, event_id):
        response = requests.get(
            self.GRAPH_API_TEMPLATE + event_id,
            params = {
                'access_token': self.facebook_token,
                'fields': ','.join(self.event_required_fields)
            }
        )

        if response.status_code != 200:
            raise InvalidEventException('Unable to retrieve event details.')

        return response.json()

    def _page_lookup(self, page_id):
        response = requests.get(
            self.GRAPH_API_TEMPLATE + page_id,
            params = {
                'access_token': self.facebook_token,
                'fields': ','.join(self.page_required_fields)
            }
        )

        if response.status_code != 200:
            raise InvalidFacebookEventPageException('Unable to retrieve page details.')

        return response.json()

    def _parse_event_data(self, event_data):
        # Checks if the event has a start and end time
        if not event_data.get('start_time', True) and not event_data.get('end_time'):
            raise InvalidEventException('Event does not have a specific start time.')

        start_dt = dateutil.parser.parse(event_data['start_time'])
        start = start_dt.astimezone(pytz.UTC)
        yesterday = (datetime.now() - timedelta(days=1)).replace(tzinfo = pytz.utc)

        # Checks if the event is in the past (compare to yesterday's date just in case)
        if start < yesterday:
            raise InvalidEventException('This event has already taken place!')

        # Checks if the event has all the other necessary fields
        if not all((key in event_data.keys()) for key in self.event_required_fields):
            raise InvalidEventException('The event is missing location or description information.')

        normalized = {
            'name': event_data['name'],
            'location': event_data['place']['name'],
            'start': start,
            'description': event_data.get('description', ''),
            'host': event_data['owner']['name'],
            'url': 'http://www.facebook.com/events/' + event_data['id']
        }

        if 'end_time' in event_data.keys():
            end_dt = dateutil.parser.parse(event_data['end_time'])
            normalized['end'] = end_dt.astimezone(pytz.UTC)

        return normalized

    def _parse_page_data(self, page_data):
        # Checks if the page has all the necessary fields
        if not all((key in page_data.keys()) for key in self.page_required_fields):
            raise InvalidFacebookEventPageException('Page missing required fields.')

        normalized = {
            'name': page_data['name'],
            'url': page_data['link'],
            'page_id': page_data['id']
        }

        return normalized

    # Public
    # Intended to be invoked by EventController#new_event
    def get_event_data(self, event_url):
        try:
            event_id = self.EVENT_LINK_TEMPLATE.match(event_url).groupdict()['event_id']
        except:
            # Validation also happens client-side so an error is unlikely to occur here
            raise InvalidEventException('Invalid url: ' + event_url)

        event_data = self._event_lookup(event_id)

        return self._parse_event_data(event_data)

    # Public
    # Intended to be invoked by FacebookEventPageController#scrape_page_events
    def get_page_event_ids(self, page_id):
        page_event_ids = []

        # First get the ids of the events that the page itself has created
        response = requests.get(
            self.GRAPH_API_TEMPLATE + page_id + '/events',
            params = {
                'access_token': self.facebook_token
            }
        )

        if response.status_code != 200:
            raise InvalidFacebookEventPageException('Unable to retrieve page event details.')

        for event_data in response.json()['data']:
            page_event_ids.append(event_data['id'])

        # Then get the ids of the events that the page has merely advertised on its wall
        response = requests.get(
            self.GRAPH_API_TEMPLATE + page_id + '/feed',
            params = {
                'access_token': self.facebook_token
            }
        )

        if response.status_code != 200:
            raise InvalidFacebookEventPageException('Unable to retrieve page event details.')

        for wall_post in response.json()['data']:
            if 'link' in wall_post and self.EVENT_LINK_TEMPLATE.match(wall_post['link']):
                page_event_ids.append(self.EVENT_LINK_TEMPLATE.match(wall_post['link']).groupdict()['event_id'])

        return page_event_ids

    # Public
    # Intended to be invoked by FacebookEventPageController#new_facebook_event_page
    def get_page_data(self, page_url):
        try:
            # Have to account for the two ways a Facebook page event URL can be formatted:
            # https://www.facebook.com/PomonaCollegeMockTrial
            # https://www.facebook.com/pages/Studio-47/146452969759
            #
            # This slice will grab either the page ID or the page username, either of which can be used to perform a Graph API lookup
            page_id = page_url.split('/')[-2]
        except:
            # Validation also happens client-side so an error is unlikely to occur here
            raise InvalidFacebookEventPageException('Invalid url: ' + page_url)

        page_data = self._page_lookup(page_id)

        return self._parse_page_data(page_data)
