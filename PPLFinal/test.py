import time
from newsapi import NewsApiClient
from datetime import date, timedelta

from bs4 import BeautifulSoup
from urllib.request import urlopen
import json, requests

newsapi = NewsApiClient(api_key='3334261d6662411b904a56968905f2bd')

from_date = time.strftime("%Y-%m-%d")
to_date = (date.today() - timedelta(days=3)).strftime("%Y-%m-%d")

for k in range(1, 5):
    all_articles = newsapi.get_everything(sources='cnn',
                                          domains='cnn.com',
                                          from_param=from_date,
                                          to=to_date,
                                          language='en',
                                          sort_by='publishedAt',
                                          page=k)
    i = 0
    for article in all_articles['articles']:
        url = article['url']
        print(url)
        print(article['urlToImage'])
        try:
            page = urlopen(url)
        except:
            i += 1

        # soup = BeautifulSoup(page, 'lxml')
        # paragraphs = soup.find_all("p", {'class': ''})
        # all_text = ''
        # if len(paragraphs) > 10:
        #     print(article['title'])
        #     print(article['description'])
        #     print(article['url'])
        #     for p in paragraphs:
        #         all_text += str(p.getText()) + " "
        #         print(p.getText())
        #
        #     print()
    print(i)