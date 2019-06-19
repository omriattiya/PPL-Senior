import pickle
import random

import nltk
from nltk import word_tokenize, sent_tokenize

pickle_model = "LinearSVC_classifier.pickle"
pickle_word_features = "word_features.pickle"
classifier = None
word_features = []


def save_pickle(filename, what_to_save):
    file = open(filename, "wb")
    pickle.dump(what_to_save, file)
    file.close()


def load_pickle(filename):
    return pickle.load(open(filename, 'rb'))


def machine_learning():
    global word_features, classifier, pickle_word_features

    negative_documents = []
    positive_documents = []

    with open("positive.txt", 'r') as csv_file:
        for record in csv_file:
            positive_documents.append((word_tokenize(record), 1))

    with open("negative.txt", 'r') as csv_file:
        for record in csv_file:
            negative_documents.append((word_tokenize(record), 0))

    pairs_pos = []
    pairs_neg = []
    for i in range(int(len(positive_documents) / 2)):
        pairs_pos.append((positive_documents[i][0] + positive_documents[i + 1][0], 1))
        i += 1

    for i in range(int(len(negative_documents) / 2)):
        pairs_neg.append((negative_documents[i][0] + negative_documents[i + 1][0], 0))
        i += 1

    positive_documents = pairs_pos
    negative_documents = pairs_neg

    documents = positive_documents + negative_documents

    random.shuffle(positive_documents)
    random.shuffle(negative_documents)
    random.shuffle(documents)

    all_words_pos = []
    all_words_neg = []

    for sentence in positive_documents:
        sentence = sentence[0]
        for word in sentence:
            all_words_pos.append(word.lower())

    for sentence in negative_documents:
        sentence = sentence[0]
        for word in sentence:
            all_words_neg.append(word.lower())

    all_words_pos = nltk.FreqDist(all_words_pos)
    all_words_neg = nltk.FreqDist(all_words_neg)

    word_features = list(set(list(all_words_pos.keys())[:3500] + list(all_words_neg.keys())[:3500]))

    save_pickle(pickle_word_features, word_features)
    print("saved word features")

    feature_sets = [(find_features(d[0]), d[1]) for d in documents]

    training_set = feature_sets[4000:]
    testing_set = feature_sets[:4000]

    accur = []
    i = 0

    classifier = nltk.NaiveBayesClassifier.train(training_set)
    accur.insert(i, nltk.classify.util.accuracy(classifier, testing_set))
    print('LinearSVC_classifier average accuracy:', sum(accur) / len(accur))

    save_pickle(pickle_model, classifier)


def find_features(tweet):
    global word_features
    words = set(tweet)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features


machine_learning()
