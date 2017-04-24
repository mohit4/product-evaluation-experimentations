"""
This script is working...
"""

import nltk
from nltk.tokenize import WordPunctTokenizer as WPT
from nltk import NaiveBayesClassifier as NBC

# word tokenizer to extract punctuations as words
wpt = WPT()

# path to dataset MUST be saved to the current directory
path = './kaggle_reviews.txt'

# dataset hold the list of words with label
dataset = []

# all words in current dataset
all_words = []

# set of feature words feeding to the classifier
word_features = []

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
    # global dataset, all_words_set, word_features
    fobj = open(path,'r')
    while True:
        text = fobj.readline()
        if text == '':
            break
        label = 'pos' if text[0] == '1' else 'neg'

        # tokenization, lower case, small words removed
        text = feature_filter([x.lower() for x in wpt.tokenize(text[2:]) if len(x)>=3])

        # hint : remove proper nouns and unneccessary words to improve accuracy
        # tagging
        # lemmatization

        # appending all words to the set
        all_words.extend(text)
        dataset.append((text,label))

    print all_words

    # now after getting the complete dataset
    # we need to extract the top words with the highest frequency
    word_features = nltk.FreqDist(all_words).keys()[:2000]

    # now working with classifier
    feature_set = [(document_features(d),c) for (d,c) in dataset]

    # taking 100 entries for testing, rest are for training
    train_set, test_set = feature_set[100:], feature_set[:100]

    # now the naive bayes classifier
    classifier = NBC.train(train_set)

    # testing
    acc = nltk.classify.accuracy(classifier, test_set)
    print 'Accuracy :',acc

    # most informative features
    classifier.show_most_informative_features(100)

    # done
    print "Done!"
