import nltk
import pickle
import random
from flask import Flask, request
from nltk import SklearnClassifier
from nltk.corpus import movie_reviews, stopwords
from nltk.tokenize import word_tokenize
from statistics import mode

app = Flask(__name__)

# pickle_model = "good_news_website/LinearSVC_classifier2.pickle"
# pickle_word_features = "good_news_website/word_features2.pickle"

pickle_model = "LinearSVC_classifier.pickle"
pickle_word_features = "word_features.pickle"
classifier = None
word_features = []


def get_ngrams(text, n):
    n_grams = nltk.ngrams(word_tokenize(text), n)
    return [' '.join(grams) for grams in n_grams]


def calc_model():
    global word_features, classifier

    documents = []

    with open("positive.txt", 'r') as csv_file:
        pos = 1
        for record in csv_file:
            documents.append((word_tokenize(record), pos))

    with open("negative.txt", 'r') as csv_file:
        for record in csv_file:
            documents.append((word_tokenize(record), 0))

    random.shuffle(documents)

    all_words = []
    for lst in documents:
        for w in lst[0]:
            all_words.append(w.lower())

    all_words = nltk.FreqDist(all_words)
    print("getting features")
    word_features = list(all_words.keys())[:5000]

    print("getting features")

    save_pickle(pickle_word_features, word_features)
    print("saved word features")

    print("setting features per tweet")
    feature_sets = [(find_features(rev), category) for (rev, category) in documents]

    testing_set = feature_sets[5000:]
    training_set = feature_sets[:5000]
    classifier = nltk.NaiveBayesClassifier.train(training_set)

    print('LinearSVC_classifier average accuracy:', nltk.classify.util.accuracy(classifier, testing_set))

    save_pickle(pickle_model, classifier)


def sentiment(text):
    feats1 = find_features(word_tokenize(text))
    return classifier.classify(feats1)


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
    votes.append(sen_text)

    try:
        ans = mode(votes)
    except Exception:
        return False
    return True if ans == 1 else False


def find_features(tweet):
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
    # word_features = load_pickle(pickle_word_features)
    # classifier = load_pickle(pickle_model)
    # classifier = load_pickle(pickle_model)
    calc_model()
