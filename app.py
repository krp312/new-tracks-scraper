"""This module downloads songs from Stereogum's new music page."""

import subprocess
import pprint
import re
import requests
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(indent=4)

# Initial links from Stereogum's /music page
url = 'https://www.stereogum.com/music/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
links = soup.find_all(attrs={"class": "image-holder pull-left"})

initial_links = []
interim_links = []
final_download_links = []

# Grouping up the first set of links to visit
for link in links:
    initial_links.append(link.a['href'])

# Visiting the first set of links
# SoundCloud iframe links are gathered in `interim_links`
# YouTube and Bandcamp links are placed into `final_download_links`
# (Bandcamp will download the whole album, for now)
# Spotify is just a string that will be passed to youtube-dl
# which totally can give undesirable results
for sublink in initial_links:
    sublink_response = requests.get(sublink)
    sublink_soup = BeautifulSoup(sublink_response.content, 'html.parser')
    if sublink_soup.find('iframe', src=re.compile('soundcloud')):
        iframe_link = sublink_soup.find('iframe', src=re.compile('soundcloud'))
        interim_links.append(iframe_link['src'])

    if sublink_soup.find('iframe', src=re.compile('youtube')):
        youtube_links = sublink_soup.find_all(
            'iframe', src=re.compile('youtube'))
        for youtube_link in youtube_links:
            final_download_links.append(youtube_link['src'])

    if sublink_soup.find('iframe', src=re.compile('open.spotify.com')):
        spotify_search_string = sublink_soup.find('meta', property="og:title")
        final_download_links.append(spotify_search_string['content'])

    if sublink_soup.find('iframe', src=re.compile('bandcamp')):
        bandcamp_download_link = sublink_soup.find(
            'a', href=re.compile('bandcamp'))
        final_download_links.append(bandcamp_download_link['href'])

# SoundCloud iframe links are visited, and final download links are extracted
for interim_link in interim_links:
    interim_link_response = requests.get(interim_link)
    if interim_link_response.status_code == 404:
        continue
    interim_link_soup = BeautifulSoup(interim_link_response.content,
                                      'html.parser')
    soundcloud = interim_link_soup.find('link', rel="canonical")
    final_download_links.append(soundcloud['href'])

# Downloads are performed
for link in final_download_links:
    if 'youtube' in link:
        subprocess.call(["youtube-dl", "-f", "bestaudio[ext=m4a]", link])
    elif 'soundcloud' in link:
        subprocess.call(['soundscrape', link])
    elif 'bandcamp' in link:
        subprocess.call(['soundscrape', '-b', link])
    else:
        subprocess.call(
            ["youtube-dl", "-f", "bestaudio[ext=m4a]", f"ytsearch:{link}"])