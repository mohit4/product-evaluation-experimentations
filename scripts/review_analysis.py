"""
script for basic review analysis using command line interpreter
"""

import sys
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
# initializing sentiment analyzer
sia = SentimentIntensityAnalyzer()

# polarity using vader sentiment analyzer (bag of words technique)
def polarity(sentence):
    ss = sia.polarity_scores(sentence)
    return ss

def keywords(text):
    # simple word tokenizer
    words = word_tokenize(text, language="english")
    tagged = nltk.pos_tag(words)
    # nouns and adjectives
    nn,jj = [],[]
    for p in tagged:
        if p[1]=="NN":
            nn.append(p[0])
        elif p[1]=="JJ":
            jj.append(p[0])
    return {'nouns':nn,'adjectives':jj}

# type 'quit' or 'exit' to stop
if __name__ == "__main__":
    text = "demo"
    while True:
        print "text>",
        text = raw_input()
        if text in ["quit","exit"]:
            sys.exit()
        kw = keywords(text)
        pol = polarity(text)
        print "Keywords "
        print "Nouns:",kw['nouns']
        print "Adjectives:",kw['adjectives']
        print "Polarity Scores"
        print "compound:",pol['compound']
        print "neg:",pol['neg']
        print "neu:",pol['neu']
        print "pos:",pol['pos']
