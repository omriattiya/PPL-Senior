import json
import time

from datetime import date, timedelta
from flask import Flask, render_template, url_for, jsonify, copy_current_request_context, redirect
from flask_socketio import SocketIO, emit
import requests, threading
from bs4 import BeautifulSoup
from urllib.request import urlopen
from newsapi import NewsApiClient

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
    time.sleep(2)


@app.errorhandler(404)
def redirect_to_main(err):
    return redirect(url_for('main'))


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

    @copy_current_request_context
    def bbc_thread():
        global stop_news_thread
        stop_news_thread = False

        from_date = date.today().strftime("%Y-%m-%d")
        to_date = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")

        for k in range(1, 3):
            all_articles = newsapi.get_everything(sources='bbc-news',
                                                  domains='bbc.co.uk',
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
                page = urlopen(url)
                soup = BeautifulSoup(page, 'lxml')
                paragraphs = soup.find_all("p", {'class': ''})
                all_text = ''
                if len(paragraphs) > 10:
                    for p in paragraphs:
                        all_text += str(p.getText()) + " "
                else:
                    continue

                news = {
                    'title': str(record['title']),
                    'url': str(record['url']),
                    'abstract': str(record['description']),
                    'thumbnail': str(record['urlToImage']),
                    'content': json.dumps(all_text)
                }
                socketio.emit('add news', news)
                print(record['title'])

    add_news_thread = threading.Thread(target=bbc_thread)
    add_news_thread.start()

    return render_template('bbc.html', files=news_files('bbc'))


@app.route('/cnn', methods=['GET', 'POST'])
def cnn():
    global add_news_thread, stop_news_thread
    stop_thread()

    @copy_current_request_context
    def cnn_thread():
        global stop_news_thread
        stop_news_thread = False

        from_date = date.today().strftime("%Y-%m-%d")
        to_date = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")

        for k in range(1, 3):
            all_articles = newsapi.get_everything(sources='cnn',
                                                  domains='cnn.com',
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
                paragraphs = soup.find_all("div", {'class': 'zn-body__paragraph'})
                all_text = ''
                if len(paragraphs) > 10:
                    for p in paragraphs:
                        all_text += str(p.getText()) + " "
                else:
                    continue

                news = {
                    'title': str(record['title']),
                    'url': str(record['url']),
                    'abstract': str(record['description']),
                    'thumbnail': str(record['urlToImage']),
                    'content': json.dumps(all_text)
                }
                socketio.emit('add news', news)
                print(record['title'])

    add_news_thread = threading.Thread(target=cnn_thread)
    add_news_thread.start()

    return render_template('cnn.html', files=news_files('cnn'))


@app.route('/nytimes', methods=['GET', 'POST'])
def new_york_times():
    global add_news_thread, stop_news_thread
    stop_thread()

    @copy_current_request_context
    def nyt_thread():
        global stop_news_thread
        stop_news_thread = False

        from_date = date.today().strftime("%Y-%m-%d")
        to_date = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")

        for k in range(1, 3):
            all_articles = newsapi.get_everything(sources='the-new-york-times',
                                                  domains='nytimes.com',
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
                paragraphs = soup.find_all("p", {'class': 'css-18icg9x'})
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
                socketio.emit('add news', news)
                print(record['title'])

    add_news_thread = threading.Thread(target=nyt_thread)
    add_news_thread.start()

    return render_template('nytimes.html', files=news_files('nyt'))


def news_files(logo_site):
    return {'background_url': url_for('static', filename='images/bg2.png'),
            'logo': url_for('static', filename='images/' + logo_site + '.png'),
            'css_news': url_for('static', filename='css/news.css'),
            'css_master': url_for('static', filename='css/master.css')}


if __name__ == '__main__':
    socketio.run(app)
