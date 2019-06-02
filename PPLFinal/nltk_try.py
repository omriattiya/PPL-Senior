
import random
from statistics import mode

import nltk
from flask import Flask, request
from nltk import SklearnClassifier
from nltk.corpus import movie_reviews, stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
from sklearn.svm import LinearSVC
from nltk.metrics.scores import (precision, recall)
from nltk import collections
import pickle

app = Flask(__name__)

# pickle_model = "PPLFinal/LinearSVC_classifier2.pickle"
# pickle_word_features = "PPLFinal/word_features2.pickle"
pickle_model = "LinearSVC_classifier4.pickle"
pickle_word_features = "word_features4.pickle"
classifier = None
word_features = []
word_features_2gram = []

def get_ngrams(text, n ):
    n_grams = nltk.ngrams(word_tokenize(text), n)
    return [ ' '.join(grams) for grams in n_grams]

def calc_model():
    global word_features, classifier, word_features_2gram
    # documents = [(list(movie_reviews.words(fileid)), category)
    #              for category in movie_reviews.categories()
    #              for fileid in movie_reviews.fileids(category)]

    stop_words = set(stopwords.words('english'))

    documents = []
    documents2gram = []

    with open("positive.txt", 'r') as csv_file:
        pos = 'pos'
        for record in csv_file:
            documents.append((word_tokenize(record), pos))
            # sixgrams = get_ngrams(record, 2)
            documents2gram.append((get_ngrams(record, 2), 1))

    with open("negative.txt", 'r') as csv_file:
        for record in csv_file:
            documents.append((word_tokenize(record), 'neg'))

            documents2gram.append((get_ngrams(record, 2), 0))


    random.shuffle(documents)
    random.shuffle(documents2gram)

    all_words = []
    for lst in documents:
        for w in lst[0]:
            # if not w in stop_words and w.isalpha():
            all_words.append(w.lower())

    all_words_2gram = []
    for lst in documents2gram:
        for w in lst[0]:
            all_words_2gram.append(w.lower())

    all_words = nltk.FreqDist(all_words)
    print("getting features")
    word_features = list(all_words.keys())[:5000]

    all_words_2gram = nltk.FreqDist(all_words_2gram)
    print("getting features")
    word_features_2gram = list(all_words_2gram.keys())[:5000]

    save_pickle(pickle_word_features, word_features)
    print("saved word features")

    print("setting features per tweet")
    feature_sets = [(find_features(rev), category) for (rev, category) in documents]
    feature_sets_2gram = [(find_features2gram(rev), category) for (rev, category) in documents2gram]



    k = 10
    cv = KFold(k)
    accur = []
    i = 0
    print("len{}".format(len(feature_sets_2gram)))
    testing_set = feature_sets[5000:] + feature_sets_2gram[5000:]
    training_set = feature_sets[:5000] + feature_sets_2gram[:5000]

    linear_svc_classifier = SklearnClassifier(LinearSVC())
    # classifier = nltk.NaiveBayesClassifier.train(testing_set)
    classifier = linear_svc_classifier.train(training_set)
    # accur.insert(i, nltk.classify.util.accuracy(classifier, testing_set))


    print('LinearSVC_classifier average accuracy:', nltk.classify.util.accuracy(classifier, testing_set))

    save_pickle(pickle_model, classifier)


def sentiment(text):
    # feats = find_features2gram(word_tokenize(text))
    feats = find_features2gram(get_ngrams(text, 2))
    return classifier.classify(feats)

    # feats = find_features2gram(get_ngrams(text, 2))
    # v = classifier.classify(feats)
    # votes.append(v)
    # return mode(votes)


def check_positive(head, abstract, text):
    global classifier, word_features
    word_features = load_pickle(pickle_word_features)
    classifier = load_pickle(pickle_model)
    sen_head = sentiment(head)
    sen_abstract = sentiment(abstract)
    sen_text = sentiment(text)
    votes = []
    votes.append(sen_head)
    votes.append(sen_abstract)
    for sentens in sent_tokenize(text):
        votes.append(sentens)
    try:
        ans = mode(votes)
    except Exception:
        return 0
    return ans



def find_features(tweet):
    global word_features
    words = set(tweet)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

def find_features2gram(tweet):
    global word_features_2gram
    words = set(tweet)
    features = {}
    for w in word_features_2gram:
        features[w] = (w in words)

    return features


def save_pickle(filename, what_to_save):
    file = open(filename, "wb")
    pickle.dump(what_to_save, file)
    file.close()


def load_pickle(filename):
    return pickle.load(open(filename, 'rb'))



if __name__ == '__main__':
    # word_features = load_pickle(pickle_word_features)
    # classifier = load_pickle(pickle_model)
    calc_model()
    # classifier = load_pickle(pickle_model)
    print(sentiment("This movie was awesome! The acting was great, plot was wonderful, and there were pythons...so yea!"))
    print(sentiment("This movie was utter junk. There were absolutely 0 pythons. I don't see what the point was at all. Horrible movie, 0/10"))
    #
    # # num_row = 0
    with open('news_texts.txt', encoding="utf8") as content_file:
        head = content_file.readline()
        print(sentiment(head))
        content = content_file.readline()
        print(sentiment(content))

    print(sentiment("Trump to hit Mexico with tariffs in anti-immigration measure"))

    # app.run(debug=True)
