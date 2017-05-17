import nltk
import sys
from nltk.corpus import wordnet

# this is a stored trained model, experiment to improve the performance
# till now it is working fine... TO TOKENIZE SENTENCE
sent_tok = nltk.data.load('tokenizers/punkt/english.pickle')

# this is the word tokenizer
from nltk.tokenize import word_tokenize

# for lemmatization
from nltk.stem.wordnet import WordNetLemmatizer as WNL
wnl = WNL()

path = '../../Filtered_Dataset/'

def fetch_data(filename):
    fobj = open(path+filename,'r')
    """
    summaries = eval(fobj.readline())
    ratings = eval(fobj.readline())
    reviews = eval(fobj.readline())
    fobj.close()
    return [summaries,ratings,reviews]
    """
    fobj.readline()
    fobj.readline()
    reviews = eval(fobj.readline())
    fobj.close()
    return reviews

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

def high_adjective_count(reviews):
    noun_score_map = {}
    for review in reviews:
        sentences = [transform([x.lower() for x in nltk.word_tokenize(sentence) if len(x)>=3]) for sentence in sent_tok.tokenize(review)]
        for sentence in sentences:
            # for each adj find the closest noun
            l = len(sentence)
            for i in range(l):
                if sentence[i][1].startswith('J'):  # if adjective
                    cl_n_i = closest_noun(sentence,i)
                    if cl_n_i >= l or cl_n_i < 0:
                        # HAC failure
                        # handle it by assigning the adjective to product
                        cl_noun = "this_product"
                    else:
                        cl_noun = sentence[cl_n_i][0]
                    # incrementing noun score or making a new entry to it
                    if not noun_score_map.has_key(cl_noun):
                        noun_score_map[cl_noun]=0
                    noun_score_map[cl_noun]+=1
            # taking threshold as average
    threshold = sum(noun_score_map.values())/len(noun_score_map)
    potential_features = {}
    for noun in noun_score_map:
        if noun_score_map[noun] >= threshold:
            potential_features[noun] = noun_score_map[noun]#threshold
    # potential_features = {key:noun_score_map[key] for key in noun_score_map if noun_score_map[key] > threshold}
    return potential_features

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    reviews = fetch_data(filename)
    pt = high_adjective_count(reviews)
    print pt
