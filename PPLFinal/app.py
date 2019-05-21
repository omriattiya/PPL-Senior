from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, emit
import time, requests, threading
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = ('https://newsapi.org/v2/top-headlines?'
       'sources=bbc-news&'
       'apiKey=3334261d6662411b904a56968905f2bd')

from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key='3334261d6662411b904a56968905f2bd')

app = Flask(__name__, template_folder="GUI")
app.config['SECRET_KEY'] = 'ppl_final'
socketio = SocketIO(app)


@socketio.on('a')  # Decorator to catch an event called "my event":
def test_message(message):  # test_message() is the event callback function.
    print(message)


@app.route('/main', methods=['GET', 'POST'])
def main():
    files = {'background_url': url_for('static', filename='images/backgroundDarker.jpg'),
             'css_main': url_for('static', filename='css/main.css'),
             'css_master': url_for('static', filename='css/master.css')}

    return render_template('main.html', files=files)


@app.route('/bbc', methods=['GET', 'POST'])
def bbc():
    # response = requests.get(url)
    # return jsonify(response.json()["articles"][0]["content"])
    #
    # # /v2/top-headlines
    # top_headlines = newsapi.get_top_headlines(sources='bbc-news')
    #
    date = time.strftime("%Y-%d-%m")
    all_articles = newsapi.get_everything(sources='bbc-news',
                                          domains='bbc.co.uk',
                                          from_param=date,
                                          to=date,
                                          language='en',
                                          sort_by='relevancy',
                                          page=2)

    files = {'background_url': url_for('static', filename='images/backgroundDarker.jpg'),
             'css_news': url_for('static', filename='css/news.css'),
             'css_master': url_for('static', filename='css/master.css'),
             'articles': all_articles}

    return render_template('bbc.html', files=files)


@app.route('/nytimes', methods=['GET', 'POST'])
def nytimes():
    # blocked_words = ["By", "Advertisement", "Supported by"]
    # source = "nyt"  # all | nyt | iht
    # section = "all"
    # time_period = "0"
    # limit = "10"
    # offset = "0"
    # api_key = "x5WGDxz9N2HToSwpoSnYHT4hNpk3psbl"
    # ny_times = "https://api.nytimes.com/svc/news/v3/content/%s/%s/%s.json?limit=%s&api-key=%s"
    # query = ny_times % (source, section, time_period, limit, api_key)
    # resp = requests.get(query)
    # data = resp.json()['results']
    # for record in data:
    #     print(record['title'])
    #     url = record['url']
    #     page = urlopen(url)
    #     soup = BeautifulSoup(page, 'lxml')
    #     paragraphs = soup.find_all("p", {'class': 'css-18icg9x'})
    #     for p in paragraphs:
    #         if p.getText() not in blocked_words:
    #             print(p.getText())
    #     print()

    files = {'background_url': url_for('static', filename='images/backgroundDarker.jpg'),
             'css_news': url_for('static', filename='css/news.css'),
             'css_master': url_for('static', filename='css/master.css')}

    return render_template('nytimes.html', files=files)


if __name__ == '__main__':
    app.run(debug=True)
