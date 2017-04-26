"""

preprocessed_dataset.py
April 25, 2017 Tuesday 5:47 pm

This script is used to preprocess the already
filtered dataset in order to achieve the following

1. Stop words removal
2. Tokenization
3. Small words filtered and all_extras removed
4. Part of Speech Tagging
5. *Subjectivity and objectivity
6. *Feature extraction

"""

# add your credits here

import nltk
import sys
import os

from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
from nltk.tokenize import WordPunctTokenizer as WPT
wpt = WPT() # word punctuation tokenizer

# path for dataset
fd_path = '../Filtered_Dataset'
rd_path = '../Preprocessed_Dataset'

filenames = []

def get_label(rating):
    if rating > 2.0:    # change this for experimentation
        return 'pos'    # currently (3-5) -> positive
    return 'neg'        # and (0-2) -> negative

# returns the list of tokenized words
def wpt_tokenization(text):
    return wpt.tokenize(text)   # currently using word punctuation tokenizer

# use this if using extra_ascii_removal filter
def word_tokenization(text):
    return nltk.word_tokenize(text) # uses nltk word tokenizer

# CAUTION : This can remove words such as not, hasn't etc neccessary for sentiment analysis
def remove_stop_words(list_of_words):
    # removing words such as not, nor, no from filter list
    # NOTE : In case of Word punctuation tokenizer add other words to filter
    discarded_words = ['no','not','nor']
    for dw in discarded_words:
        stop.discard(dw)
    return [x.lower() for x in list_of_words if x.lower() not in stopwords]

# remove all the extra ascii characters
def extra_ascii_removal(list_of_words):
    l = len(list_of_words)
    for i in range(l):
        list_of_words[i] = ''.join(x for x in list_of_words[i] if ord(x) < 128)
    return list_of_words

def preprocess(filename):
    fobj = open(filename,'r')
    summary = eval(fobj.readline())
    ratings = eval(fobj.readline())
    reviews = eval(fobj.readline())
    no_of_reviews = len(ratings)
    for i in range(no_of_reviews):
        label = get_label(ratings[i])
        review = reviews[i]
        tokens = extra_ascii_removal(word_tokenization(review))


if __name__ == "__main__":

    # checking if the dataset to be working upon exists or not
    print "Current Directory :",os.getcwd()
    print "Checking for Filtered Dataset..."
    if not os.path.isdir(fd_path):
        print "Not found!"
        print "Run 'filter_dataset.py'"
        print "Exiting..."
        sys.exit()

    # fetching the filenames
    filenames = os.listdir(fd_path)

    # creating directory for result dataset
    if not os.path.isdir(rd_path):
        os.mkdir(rd_path)

    # performing preprocessing for each file
    for filename in filenames:
        preprocessed(filename)
