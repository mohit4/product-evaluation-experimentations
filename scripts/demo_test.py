"""
This script loads the classifier saved and use it to classify text
"""

import nltk
from nltk.tokenize import WordPunctTokenizer as WPT
from nltk import NaiveBayesClassifier as NBC
import pickle

# word tokenizer to extract punctuations as words
wpt = WPT()

# all words in current dataset
all_words = []

# set of feature words feeding to the classifier
word_features = []

# reloads the classifier in memory
def load_classifier(pickle_file):
    f = open(pickle_file,'rb')
    classifier = pickle.load(f)
    f.close()
    return classifier

# filtering out the unneccessary words
def feature_filter(list_of_words):
    # acceptable = ['CC','DT','IN','JJ','JJR','JJS','MD','NNS','PDT','RB','RBR','RBS','RP','UH','VB','VBD','VBG','VBN','VBP','VBZ']
    acceptable = ['JJ','JJR','JJS','RB','RBR','RBS','RP','VB','VBD','VBG','VBN','VBP','VBZ']
    resulting_words = []
    tagged_words = nltk.pos_tag(list_of_words)
    for p in tagged_words:
        if p[1] in acceptable:
            resulting_words.append(p[0])
    return resulting_words

# document feature extractor
def document_features(list_of_words):
    # global word_features
    document_words = set(list_of_words)
    features = {}
    for word in word_features:
        features['contains(%s)'%word] = (word in list_of_words)
    return features

if __name__ == "__main__":
    classifier = load_classifier('naive_bayes_classifier.pickle')
    while True:
        text = raw_input("Enter review or 'quit' :")
        if text == 'quit':
            break
        label = classifier.classify(document_features(feature_filter(wpt.tokenize(text))))
        print "Label...",label
        print ''
