"""Is this the right way to do a docstring?"""

import pprint
import requests
from bs4 import BeautifulSoup
import re
import soundscrape

pp = pprint.PrettyPrinter(indent=4)

url = 'https://www.stereogum.com/music/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
links = soup.find_all(attrs={"class": "image-holder pull-left"})

initial_links = []
for link in links:
    initial_links.append(link.a['href'])

link1 = initial_links[0]
response1 = requests.get(link1)
soup1 = BeautifulSoup(response1.content, 'html.parser')
iframe = soup1.find_all('iframe', src=re.compile("soundcloud"))
pp.pprint(iframe[0]['src'])