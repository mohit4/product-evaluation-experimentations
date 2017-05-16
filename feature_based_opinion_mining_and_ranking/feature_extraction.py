"""
a feature extraction based on HAC algorithm
"""


import nltk
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer as WNL
wnl = WNL()

sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# toggle debugging here
# or give command line argument -d
debugging = False

# assistant to lemmatization
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

# lemmatizes the word with appropriate pos tag
def lemmatization(word,pos):
    wn_pos = get_wordnet_pos(pos)
    if wn_pos=='':
        return word
    return wnl.lemmatize(word,wn_pos)

# sentence is a list of words
# working on a single sentence and lemmatize the words wherever possible
# returns a list of word,pos-tag pair
def transform(sentence):
    l = len(sentence)
    # part of speech tagging
    tags = nltk.pos_tag(sentence)
    for i in xrange(l):
        sentence[i] = (lemmatization(tags[i][0],tags[i][1]),tags[i][1])
    return sentence

# this functions returns the index of the closest noun to the given adjective
def closest_noun(sentence,adjective_index):
    i = j = adjective_index
    l = len(sentence)
    while i>=0 and not (sentence[i][1].startswith('N') or sentence[i][1].startswith('PR')):
        i-=1
    while j<l and not (sentence[j][1].startswith('N') or sentence[j][1].startswith('PR')):
        j+=1
    # check the absolute distance from the current adjective
    if abs(i-adjective_index) > abs(j-adjective_index):
        return j    # return the smaller distance
    return i

# reviews is a list of strings containing multiple sentences
def high_adjective_count(reviews):
    noun_score_map = {}
    for review in reviews:
        # this sentence contains words that are lemmatized
        sentences = [transform(nltk.word_tokenize(sentence)) for sentence in sentence_tokenizer.tokenize(review)]
        for sentence in sentences:
            # for each adj find the closest noun
            l = len(sentence)
            for i in range(l):
                if sentence[i][1].startswith('J'):  # if adjective
                    cl_n_i = closest_noun(sentence,i)
                    if cl_n_i >= l or cl_n_i < 0:
                        cl_n_i = i
                        print "hac failure!"
                    if debugging:
                        print cl_n_i
                    cl_noun = sentence[cl_n_i][0]  # find the closest noun
                    if not noun_score_map.has_key(cl_noun):
                        noun_score_map[cl_noun]=0
                    noun_score_map[cl_noun]+=1
    # taking the threshold as average
    threshold = sum(noun_score_map.values())/len(noun_score_map)
    potential_features = {key:noun_score_map[key] for key in noun_score_map if noun_score_map[key] > threshold}
    return potential_features

# opens a file and return the len,summaries,ratings and reviews
def get_attr(filename):
    fobj = open(filename,'r')
    sm = eval(fobj.readline())
    rt = eval(fobj.readline())
    rv = eval(fobj.readline())
    fobj.close()
    return (len(rt),sm,rt,rv)

if __name__ == "__main__":

    import os
    import sys
    import timeit
    if sys.argv[-1]=='-d':
        debugging=True

    start = timeit.default_timer()

    fd_path = '../../Filtered_Dataset'
    filenames = os.listdir(fd_path)[:1000]  # listing first 1000 files only
    os.chdir(fd_path)

    for filename in filenames:
        attr = get_attr(filename)
        pt = high_adjective_count(attr[3])
        print filename,pt

    print "time taken :",timeit.default_timer() - start,"sec(s)"
