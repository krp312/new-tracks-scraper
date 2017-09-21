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
for link in links:
    initial_links.append(link.a['href'])

final_download_links = []
iframe_addresses = []

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

pp.pprint(final_download_links)
pp.pprint(iframe_addresses)