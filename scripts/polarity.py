"""
Python script for evaluating the polarity of the given sentence
using nltk vader sentiment analyzer
"""

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sys

# initializing sentiment analyzer
sia = SentimentIntensityAnalyzer()

def polarity(sentences):
    for sentence in sentences:
        print sentence
        ss = sia.polarity_scores(sentence)
        for k in sorted(ss):
            print '{0}: {1}, '.format(k, ss[k])

# provide the sentence as a single command line argument or a list of arguments
if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print "No sentence or list of sentenses specified!"
    elif len(sys.argv) == 2:
        sent = sys.argv[1]
        polarity([sent])
    elif len(sys.argv) > 2:
        polarity(eval(sys.argv[2]))
