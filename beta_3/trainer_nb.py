"""

trainer_nb.py
April 27, 2017 Thursday 3:57 pm

This script is used to train the naive bayes Classifier
using the preprocessed_dataset and saves the Classifier
to a pickle file

"""

# add your credits here
__author__ = "Mohit Kumar"
__version__ = "0.9.3"   # beta 3
__maintainer__ = "Mohit Kumar"
__email__ = "mohitkumar2801@gmail.com"
__status__ = "Production"

import nltk
import pickle
import os
import sys

from nltk import NaiveBayesClassifier as NBC

debugging = False

all_words = []
dataset = []

rd_path = '../../Preprocessed_Dataset'
id_path = '../../Feature_Dataset'

# to save the classifier for later use
def save_classifier(classifier):
    f = open('naive_bayes_classifier.pickle','wb')
    pickle.dump(classifier,f)
    f.close()
    print "classifier saved!"

# this will extract the list of features from a document
# returns a dictionary with the given format
# <word1> : True
# <word2> : False
# ...
# <wordn> : True
def document_features(list_of_words):
    document_words = set(list_of_words)
    features = {}
    for word in word_features:
        features[word]=(word in list_of_words)
    return features

def fetch_features(filename):
    fobj = open(rd_path+'/'+filename,'r')
    list_of_reviews = eval(fobj.readline())
    fobj.close()
    l = len(list_of_reviews)
    for ii in range(l):
        current_words = [list_of_reviews[ii][0][i][0] for i in range(len(list_of_reviews[ii][0]))]
        all_words.extend(current_words)
        dataset.append((current_words,list_of_reviews[ii][1]))

if __name__ == "__main__":

    # checking if the dataset to be working upon exists or not
    print "Current Directory :",os.getcwd()
    print "Checking for Preprocessed Dataset..."
    if not os.path.isdir(rd_path):
        print "Not found!"
        print "Run 'preprocessed_dataset.py'"
        print "Exiting..."
        sys.exit()

    # fetching the filenames
    if debugging:
        print "Listing file names..."
    filenames = os.listdir(rd_path)
    total_files = 4000#len(filenames)

    print "Fetching data..."
    for i in range(total_files):
        fetch_features(filenames[i])
    print "done"

    print "Evaluating features..."
    # taking most frequent first words
    no_of_features = 2000
    word_features = nltk.FreqDist(all_words).keys()[:no_of_features]
    fobj2 = open('most_frequent_features.txt','w')
    fobj2.write(str(word_features))
    fobj2.close()
    print "done"

    # all features
    feature_set = [(document_features(d),c) for (d,c) in dataset]

    # ratio for training to testing
    train_set = 0.20
    test_set = 0.20

    print "training classifier..."
    # classifier
    classifier = NBC.train(feature_set[:train_set*len(feature_set)])
    print "done"

    # testing
    acc = nltk.classify.accuracy(classifier, feature_set[test_set*len(feature_set):])
    print "accuracy :",acc

    # saving classifier
    print "saving classifier..."
    save_classifier(classifier)

    # Done
    print "Done!"
