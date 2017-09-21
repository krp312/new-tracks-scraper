"""Is this the right way to do a docstring?"""

import pprint
import requests
from bs4 import BeautifulSoup
import re
import soundscrape

pp = pprint.PrettyPrinter(indent=4)

# initial links from stereogum's /music page
url = 'https://www.stereogum.com/music/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
links = soup.find_all(attrs={"class": "image-holder pull-left"})

initial_links = []
iframe_addresses = []
final_download_links = []

# grouping up the first set of links to visit
for link in links:
    initial_links.append(link.a['href'])

# visiting the first set of links
# soundcloud iframe links are gathered in `iframe_addresses`
#   one more step before their final download links
# youtube links are placed into `final_download_links`
for sublink in initial_links:
    sublink_response = requests.get(sublink)
    sublink_soup = BeautifulSoup(sublink_response.content, 'html.parser')
    if sublink_soup.find('iframe', src=re.compile('soundcloud')):
        iframe_address = sublink_soup.find(
            'iframe', src=re.compile('soundcloud'))
        iframe_addresses.append(iframe_address['src'])

    if sublink_soup.find('iframe', src=re.compile('youtube')):
        youtube_link = sublink_soup.find('iframe', src=re.compile('youtube'))
        final_download_links.append(youtube_link['src'])

# soundcloud iframe links are visited, and final download links are extracted
for address in iframe_addresses:
    address_response = requests.get(address)
    if address_response.status_code == 404:
        continue
    address_soup = BeautifulSoup(address_response.content, 'html.parser')
    soundcloud = address_soup.find('link', rel="canonical")
    final_download_links.append(soundcloud['href'])
