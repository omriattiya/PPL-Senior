import json
import threading
from bs4 import BeautifulSoup
from datetime import date, timedelta
from flask import Flask, render_template, url_for, redirect
from flask_socketio import SocketIO
from newsapi import NewsApiClient
from urllib.request import urlopen

import ModelNltk

# INIT :D
add_news_thread = None
stop_news_thread = False
newsapi = NewsApiClient(api_key='3334261d6662411b904a56968905f2bd')
app = Flask(__name__, template_folder="GUI")
app.config['SECRET_KEY'] = 'ppl_final'
socketio = SocketIO(app)


@socketio.on('connected')
def test_message(message):
    print(message)


@socketio.on('stop')
def stop_thread():
    global stop_news_thread
    stop_news_thread = True
    if add_news_thread is not None:
        add_news_thread.join()


@app.route('/main', methods=['GET', 'POST'])
def main():
    stop_thread()
    files = {'background_url': url_for('static', filename='images/bg2.png'),
             'css_main': url_for('static', filename='css/main.css'),
             'css_master': url_for('static', filename='css/master.css')}

    return render_template('main.html', files=files)


@app.route('/bbc', methods=['GET', 'POST'])
def bbc():
    global add_news_thread, stop_news_thread
    stop_thread()

    sources = 'bbc-news'
    domains = 'bbc.co.uk'
    element = 'p'
    class_to_find = ''

    add_news_thread = threading.Thread(target=news_thread, args=(sources, domains, element, class_to_find))
    add_news_thread.start()

    return render_template('bbc.html', files=news_files('bbc'))


@app.route('/cnn', methods=['GET', 'POST'])
def cnn():
    global add_news_thread, stop_news_thread
    stop_thread()

    sources = 'cnn'
    domains = 'cnn.com'
    element = 'div'
    class_to_find = 'zn-body__paragraph'

    add_news_thread = threading.Thread(target=news_thread, args=(sources, domains, element, class_to_find))
    add_news_thread.start()

    return render_template('cnn.html', files=news_files('cnn'))


@app.route('/nytimes', methods=['GET', 'POST'])
def new_york_times():
    global add_news_thread, stop_news_thread
    stop_thread()

    sources = 'the-new-york-times'
    domains = 'nytimes.com'
    element = 'p'
    class_to_find = 'css-18icg9x'

    add_news_thread = threading.Thread(target=news_thread, args=(sources, domains, element, class_to_find))
    add_news_thread.start()

    return render_template('nytimes.html', files=news_files('nyt'))


def news_files(logo_site):
    return {'background_url': url_for('static', filename='images/bg2.png'),
            'logo': url_for('static', filename='images/' + logo_site + '.png'),
            'css_news': url_for('static', filename='css/news.css'),
            'css_master': url_for('static', filename='css/master.css'),
            'js_news': url_for('static', filename='news.js')}


def news_thread(sources, domains, element_to_find, class_to_find):
    global stop_news_thread
    stop_news_thread = False

    from_date = date.today().strftime("%Y-%m-%d")
    to_date = (date.today() - timedelta(days=5)).strftime("%Y-%m-%d")

    for k in range(1, 5):
        all_articles = newsapi.get_everything(sources=sources,
                                              domains=domains,
                                              from_param=from_date,
                                              to=to_date,
                                              language='en',
                                              sort_by='publishedAt',
                                              page=k)
        for record in all_articles['articles']:
            if stop_news_thread:
                stop_news_thread = False
                return
            url = record['url']
            try:
                page = urlopen(url)
            except:
                continue
            soup = BeautifulSoup(page, 'lxml')
            paragraphs = soup.find_all(element_to_find, {'class': class_to_find})
            all_text = ''
            for p in paragraphs:
                all_text += str(p.getText()) + " "

            news = {
                'title': str(record['title']),
                'url': str(record['url']),
                'abstract': str(record['description']),
                'thumbnail': str(record['urlToImage']),
                'content': json.dumps(all_text)
            }
            if ModelNltk.check_positive(news['title'], news['abstract'], all_text):
                socketio.emit('add news', news)
            else:
                print(record['title'])
                print(record['url'])
                print()


if __name__ == '__main__':
    socketio.run(app)
