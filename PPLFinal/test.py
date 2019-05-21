from bs4 import BeautifulSoup
from urllib.request import urlopen
import json, requests

blocked_words = ["By", "Advertisement", "Supported by"]

source = "nyt"  # all | nyt | iht
section = "all"
time_period = "0"
limit = "10"
offset = "0"
api_key = "x5WGDxz9N2HToSwpoSnYHT4hNpk3psbl"
ny_times = "https://api.nytimes.com/svc/news/v3/content/%s/%s/%s.json?limit=%s&api-key=%s"
query = ny_times % (source, section, time_period, limit, api_key)
resp = requests.get(query)
data = resp.json()['results']
for record in data:
    print(record['title'])
    url = record['url']
    page = urlopen(url)
    soup = BeautifulSoup(page, 'lxml')
    paragraphs = soup.find_all("p", {'class': 'css-18icg9x'})
    for p in paragraphs:
        if p.getText() not in blocked_words:
            print(p.getText())
    print()
