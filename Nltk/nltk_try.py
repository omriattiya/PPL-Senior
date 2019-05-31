import re
import csv
import random
from statistics import mode

import nltk
import numpy as np
from flask import Flask, request
from nltk import SklearnClassifier
from nltk.corpus import movie_reviews
from nltk.tokenize import word_tokenize
from sklearn.model_selection import KFold
from sklearn.svm import LinearSVC
from nltk.metrics.scores import (precision, recall)
from nltk import collections
import pickle

app = Flask(__name__)

pickle_model = "LinearSVC_classifier.pickle"
pickle_word_features = "word_features.pickle"
classifier = None
word_features = []


def calc_model():
    global word_features, classifier
    documents = [(list(movie_reviews.words(fileid)), category)
                 for category in movie_reviews.categories()
                 for fileid in movie_reviews.fileids(category)]

    random.shuffle(documents)

    all_words = []
    for w in movie_reviews.words():
        all_words.append(w.lower())

    all_words_2gram = []
    # for w in movie_reviews:
    #     sixgrams = nltk.ngrams(w.split(), 2)
    #     all_words_2gram.append(w.lower())

    all_words = nltk.FreqDist(all_words)
    print("getting features")
    word_features = list(all_words.keys())[:5000]

    save_pickle(pickle_word_features, word_features)
    print("saved word features")

    print("setting features per tweet")
    feature_sets = [(find_features(rev), category) for (rev, category) in documents]



    k = 10
    cv = KFold(k)
    accur = []
    i = 0

    testing_set = feature_sets[1900:]
    training_set = feature_sets[:1900]

    linear_svc_classifier = SklearnClassifier(LinearSVC())
    classifier = linear_svc_classifier.train(testing_set)
    accur.insert(i, nltk.classify.util.accuracy(classifier, training_set))


    print('LinearSVC_classifier average accuracy:', sum(accur) / len(accur))

    # save_pickle(pickle_model, classifier)


def sentiment(text):
    feats = find_features(word_tokenize(text))
    votes = []
    v = classifier.classify(feats)
    votes.append(v)
    return mode(votes)


def find_features(tweet):
    global word_features
    words = set(tweet)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

def find_features2gram(tweet):
    global word_features
    words = set(tweet)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features


def save_pickle(filename, what_to_save):
    file = open(filename, "wb")
    pickle.dump(what_to_save, file)
    file.close()


def load_pickle(filename):
    return pickle.load(open(filename, 'rb'))



if __name__ == '__main__':
    calc_model()
    # classifier = load_pickle(pickle_model)
    print(sentiment("This movie was awesome! The acting was great, plot was wonderful, and there were pythons...so yea!"))
    print(sentiment("This movie was utter junk. There were absolutely 0 pythons. I don't see what the point was at all. Horrible movie, 0/10"))

    # num_row = 0
    with open('report.txt', 'r') as content_file:
        head = content_file.readline()
        print(sentiment(head))
        content = content_file.readline()
        print(sentiment(content))

    print(sentiment("Trump to hit Mexico with tariffs in anti-immigration measure"))

    # app.run(debug=True)
