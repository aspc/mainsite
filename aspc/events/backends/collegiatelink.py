import requests
import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)

class CollegiateLinkBackend(object):
    rss_url = 'https://claremont.collegiatelink.net/EventRss/EventsRss';

    def _get_rss(self):
        events_xml_tree = requests.get(self.rss_url).text
        return ET.fromstring(events_xml_tree)

    def get_events_data(self):
        normalized_events = []

        events_xml_root = self._get_rss()

        for item in events_xml_root.iter('item'):
            event = {
                'name': item.find('title').text,
                'location': None,
                'start': 'blah',
                'description': item.find('description').text,
                'host': item.find('author').text,
                'url': item.find('link').text,
            }
            normalized_events.append(event)

        return normalized_events