"""
This script is used for testing various stemming algorithms provided by the nltk

Friday 7 April 2017 12:12:17 AM IST

"""

# importing the nltk corpus for test data
import nltk.corpus as ncp
# using the brown corpus - contains 500 text files
from ncp import brown

"""
Stemming algorithms have least accuracy
uncomment the code in case needed to use the stemmer
"""
# stemmer based on the Porter Stemming Algorithm
from nltk.stem.porter import PorterStemmer
# stemmer based on Lancaster Stemming Algorithm
from nltk.stem.lancaster import LancasterStemmer
# stemmer based on Snowball Stemming Algorithm
from nltk.stem import SnowballStemmer

"""
Accuracy is achieved using WordNet Lemmatizer
"""
# wordnet lemmatizer
from nltk.stem import WordNetLemmatizer as WNL
# the word net lemmatizer object
wnl = WNL()
"""
The lemmatizer's default pos argument is 'n' i.e. noun
specify the pos as pos='v' for verb
"""

"""
method to print result based on lemmatization
w - single word
p - pos
    n - noun
    a - adjective/adverb
    v - verb
"""
def lemma(w,p='n'):
    return wnl.lemmatize(w,p)

if __name__ == "__main__":
    # testing on sentences from brown corpus
    sentences = brown.sents(brown.fileids()[0])
    for sentence in sentences:
        for i in range(len(sentence)):
            # to be continued...
