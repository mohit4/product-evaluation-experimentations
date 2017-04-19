"""
This is a test script that I made for movie reviews sentiment analysis as the
dataset for movie reviews was provided by nltk itself.
I will apply the algorithm to product reviews once I get a better labelled
dataset :)
"""

import nltk
from nltk.corpus import movie_reviews
from random import shuffle

# toggle debugging here
debugging = False

# fetching the movie_reviews words along with categories
print "Fetching movie reviews...",
documents = [(list(movie_reviews.words(fileid)), category) for category in movie_reviews.categories() for fileid in movie_reviews.fileids(category)]
print "Done"

shuffle(documents)

if debugging:
    print documents[0]  # for debugging purpose
    len(documents)  # ...

# making a list of most frequent words in the entire corpus
print "Calculating frequency...",
all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
print "Done"

# taking the top 2000 most frequent words
word_features = all_words.keys()[:2000]

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)'%word] = (word in document_words)
    return features

# generated feature sets for movie reviews documents
print "Generating feature set...",
featuresets = [(document_features(d), c) for (d,c) in documents]
print "Done"

# splitting the dataset for training and testing
train_set, test_set = featuresets[100:], featuresets[:100]

# training a naive bayes classifier with train set
print "Training the classifier...",
classifier = nltk.NaiveBayesClassifier.train(train_set)
print "Done!"

# for printing the accuracy on test set
print "Testing..."
acc = nltk.classify.accuracy(classifier, test_set)
print "Accuracy on test set :",acc
print "Ready to accept reviews! Enter 'quit' to exit."
print "> ",

import sys

while True:
    text = raw_input()
    if text == "quit":
        sys.exit(0)
    text_features = document_features(text.split())
    polarity = classifier.classify(text_features)
    print polarity
