#!/usr/bin/env python

"""
naive_bayes_classifier.py : used for training and testing the dataset

input -
    naive_bayes_classifier.py <dataset name> <train>:<test>

output -
    log file : naive_bayes_classifier_log.txt
    saved classifier : nbc_<datetime>.pickle

"""

__author__ = "Mohit Kumar"

dataset = "./dataset/kaggle_reviews.txt"

training_ratio = 80

reviews = []

import nltk, sys
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer as WNL

def remove_non_ascii(word):
    return ''.join(i for i in word if ord(i)<128)

def lemmatize(list_of_words):
    tagged_words = nltk.pos_tag(list_of_words)
    for pair in tagged_words:


def filter(text):
    words = word_tokenize(text)
    words = [remove_non_ascii(x) for x in words if len(x)>=3]
    words =
    return ''.join(words)

def fetch_reviews():
    fobj = open(dataset,'r')
    while True:
        text = fobj.readline()
        label = 'pos' if text[0]=='1' else 'neg'
        text = filter(text[2:])

import sys

if __name__ == "__main__":
