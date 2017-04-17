from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *

# no of instances required
n_instances = 100

# each document is represented by a tuple (sentence,label)
# tokenized sentence is represented by list of strings
subj_docs = [(sent,'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]

# to split the training and testing data
train_subj_docs = subj_docs[:80]
test_subj_docs = subj_docs[80:100]
train_obj_docs = obj_docs[:80]
test_obj_docs = obj_docs[80:100]

training_docs = train_subj_docs + train_obj_docs
testing_docs = test_subj_docs + test_obj_docs

# initializing the SentimentAnalyzer
sentiment_analyzer = SentimentAnalyzer()
all_words_neg = sentiment_analyzer.all_words([mark_negation(doc) for doc in training_docs])

# handling negations using simple unigram word features
unigram_feats = sentiment_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
sentiment_analyzer.add_feat_extractor(extract_unigram_feats, unigram=unigram_feats)

# features are applied to obtain a feature value representation of the dataset
training_set = sentiment_analyzer.apply_features(training_docs)
test_set = sentiment_analyzer.apply_features(testing_docs)

# training and output
trainer = NaiveBayesClassifier.train
classifier = sentiment_analyzer.train(trainer, training_set)

for key,value in sorted(sentiment_analyzer.evaluate(test_set).items()):
    print '{0}: {1}'.format(key, value)
