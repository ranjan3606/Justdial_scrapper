import requests
from bs4 import BeautifulSoup

getpage= requests.get('http://form.hktdc.com/UI_VisitorIntranet/Public/VisitorListPublic.aspx?EVENTID=588916b5-631b-4d63-a828-26d727e8011f&LANGID=1')

getpage_soup= BeautifulSoup(getpage.text, 'html.parser')

all_links= getpage_soup.findAll('a')

for link in all_links:
    print (link)
