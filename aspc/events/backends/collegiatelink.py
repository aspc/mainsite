import requests
import xml.etree.ElementTree as ET
import logging
from datetime import datetime
from HTMLParser import HTMLParser
import re
from aspc.events.exceptions import InvalidEventException

logger = logging.getLogger(__name__)

class CollegiateLinkBackend(object):
    required_fields = ('location', 'start', 'description') # 'name' is also required but check for it in a different way
    rss_url = 'https://claremont.collegiatelink.net/EventRss/EventsRss';

    def _get_rss(self):
        events_xml_tree = requests.get(self.rss_url).text
        return ET.fromstring(events_xml_tree.encode('ascii', 'ignore')) # CollegiateLink doesn't deign to provide proper ascii text, so re-encode it

    def get_events_data(self):
        normalized_events = []

        events_xml_root = self._get_rss()

        for item in events_xml_root.iter('item'):
            # Checks for the event title
            if not item.find('title').text or item.find('title').text == '':
                raise InvalidEventException('Event does not have a title time.')

            event = {
                'name': item.find('title').text,
                'url': item.find('link').text,
            }

            # CollegiateLink provides poorly-formed HTML in its RSS feed, so it is necessary to further parse it
            parser = CollegiateLinkHTMLParser()
            parser.feed(item.find('description').text)
            if parser.parsed_data['start'] == '': # If the event doesn't have a date, don't add it to the calendar
                continue

            # Checks if the parsed data includes all the necessary fields
            if not all((key in parser.parsed_data.keys()) for key in self.required_fields):
                raise InvalidEventException('Unable to retrieve page details.')

            event['location'] = parser.parsed_data['location']
            event['description'] = parser.parsed_data['description']
            event['start'] = datetime.strptime(parser.parsed_data['start'], '%A, %B %d, %Y (%I:%M %p)')

            # The host is oddly wrapped inside of parentheses... need to extract it
            event['host'] = (re.search(r'\((.*?)\)', item.find('author').text)).group(1)

            normalized_events.append(event)

        return normalized_events


class CollegiateLinkHTMLParser(HTMLParser):
    parsed_data = {
        'start': '',
        'location': '',
        'description': ''
    }
    __current_state = None

    def handle_starttag(self, tag, attrs):
        if ('class', 'dtstart') in attrs:
            self.__current_state = 'start'
        elif ('class', 'location') in attrs:
            self.__current_state = 'location'
        elif ('class', 'description') in attrs:
            self.__current_state = 'description'
        else:
            if self.__current_state != 'description': # The description block has a lot of tags inside of it, so this captures nested information
                self.__current_state = ''

    def handle_endtag(self, tag):
        if self.__current_state != 'description': # The description block has a lot of tags inside of it, so this captures nested information
            self.__current_state = ''

    def handle_data(self, data):
        if self.__current_state == 'start':
            self.parsed_data['start'] = data
        elif self.__current_state == 'location':
            self.parsed_data['location'] = data
        elif self.__current_state == 'description':
            self.parsed_data['description'] = data