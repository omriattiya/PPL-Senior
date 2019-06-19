# python-development-tools
In these repository there are all the assignments, labs and final project of the Principles of Programming Languages elective course at spring 2019 at ,Ben Gurion University, Israel.
The course included 2 home assignments, 2 labs and 1 final project.

# Final Project - The Good News Website
## ABSTRACT
We live in an industrialized, complex and dangerous world. Most of the things that interest the public are topics like: survival, politics and extreme things that happened just around the corner. Unfortunately, most of these things are bad news. These news are reported in media like: TV's, radio and news sites. Most of the news are frightening, sad or stressful. This creates a displacement of the good and pleasant news from our lives. 
> "We want to create a platform that filtered out the negative news and thus gave the user a nice experience of reading the news."

## CHALLENGES
We had 2 main challenges in the project:
1. Creating a website and bringing news.
2. Machine Learning & Sentiment Analysis.

### WEBSITE & NEWS
##### WEBSITE
- Client side: pure HTML
- Server side: python using Flask library
##### NEWS
In order to get news we used [News API](https://github.com/mattlisiv/newsapi-python).
This API gives us headlines and URL's for news, at real time, from a certain website (i.e. BBC, CNN, NYTIMES, etc).
We used [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) for extracting news content and then we are passing it to our classifier.

### MACHINE LEARNING & SENTIMENT ANALYSIS
##### DATASET
Our dataset is composed of 5000 negaive sentences and 5000 positive sentences and can be found [here](https://www.kaggle.com/chaitanyarahalkar/positive-and-negative-sentences).
##### CLASSIFIER
After trying diffrent approaches like: removing stopwords, stemming, 2-gram and counting possitive and negative words (which all led to bad results), we decided to extract features as the most 5000 common words form our dataset.
We used NLTK Native Bayes for our classifier and we achieved 75% accurecy.

## Installing
The project is running with python 3.6^.
After downloading the [good news website folder](https://github.com/omriattiya/python-development-tools/tree/master/good_news_website) you need to install the following libraries:
```
pip install flask-socketio
pip install newsapi-pyhton
pip install nltk
pip install beautifulsoup4
pip install flask
```
## Deployment 
```
cd good_news_website
python -m flask run
```
Wait a few seconds until you see the line
> *Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Now the server is running and you can access it in [http://127.0.0.1:5000/main](http://127.0.0.1:5000/main)

## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used
* [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/) - Used for bi-directional communications between the clients and the server.
* [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) - Used for extracting news content
* [NLTK](https://www.nltk.org/) - Used for creating our classifier
* [News API](https://github.com/mattlisiv/newsapi-python) - Used for retrieving news headlines data


## Contributing
- Omri Attiya - *initial work & client side* - [@github/omriattiya](https://github.com/omriattiya)
- Shira Ezra - *machine learning classifier* - [@github/shiraez](https://github.com/shiraez)

For more details see [contributors](https://github.com/omriattiya/python-development-tools/graphs/contributors).
