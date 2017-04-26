"""

preprocessed_dataset.py
April 25, 2017 Tuesday 5:47 pm

This script is used to preprocess the already
filtered dataset in order to achieve the following

1. Stop words removal                           DONE
2. Tokenization                                 DONE
3. Small words filtered and all_extras removed  DONE
4. Part of Speech Tagging                       DONE
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
# check for the case where a word contains all non ascii characters
def extra_ascii_removal(list_of_words):
    l = len(list_of_words)
    for i in range(l):
        list_of_words[i] = ''.join(x for x in list_of_words[i] if ord(x) < 128)
    return list_of_words

"""
List of tags -

CC: conjunction, coordinating

& 'n and both but either et for less minus neither nor or plus so
therefore times v. versus vs. whether yet

CD: numeral, cardinal

mid-1890 nine-thirty forty-two one-tenth ten million 0.5 one forty-
seven 1987 twenty '79 zero two 78-degrees eighty-four IX '60s .025
fifteen 271,124 dozen quintillion DM2,000 ...

DT: determiner

all an another any both del each either every half la many much nary
neither no some such that the them these this those

EX: existential there

there

IN: preposition or conjunction, subordinating

astride among uppon whether out inside pro despite on by throughout
below within for towards near behind atop around if like until below
next into if beside ...

JJ: adjective or numeral, ordinal

third ill-mannered pre-war regrettable oiled calamitous first separable
ectoplasmic battery-powered participatory fourth still-to-be-named
multilingual multi-disciplinary ...

JJR: adjective, comparative

bleaker braver breezier briefer brighter brisker broader bumper busier
calmer cheaper choosier cleaner clearer closer colder commoner costlier
cozier creamier crunchier cuter ...

JJS: adjective, superlative

calmest cheapest choicest classiest cleanest clearest closest commonest
corniest costliest crassest creepiest crudest cutest darkest deadliest
dearest deepest densest dinkiest ...

LS: list item marker

A A. B B. C C. D E F First G H I J K One SP-44001 SP-44002 SP-44005
SP-44007 Second Third Three Two * a b c d first five four one six three
two

MD: modal auxiliary

can cannot could couldn't dare may might must need ought shall should
shouldn't will would

NN: noun, common, singular or mass

common-carrier cabbage knuckle-duster Casino afghan shed thermostat
investment slide humour falloff slick wind hyena override subhumanity
machinist ...

NNP: noun, proper, singular

Motown Venneboerger Czestochwa Ranzer Conchita Trumplane Christos
Oceanside Escobar Kreisler Sawyer Cougar Yvette Ervin ODI Darryl CTCA
Shannon A.K.C. Meltex Liverpool ...

NNS: noun, common, plural

undergraduates scotches bric-a-brac products bodyguards facets coasts
divestitures storehouses designs clubs fragrances averages
subjectivists apprehensions muses factory-jobs ...

PDT: pre-determiner

all both half many quite such sure this

POS: genitive marker

' 's

PRP: pronoun, personal

hers herself him himself hisself it itself me myself one oneself ours
ourselves ownself self she thee theirs them themselves they thou thy us

PRP$: pronoun, possessive

her his mine my our ours their thy your

RB: adverb

occasionally unabatingly maddeningly adventurously professedly
stirringly prominently technologically magisterially predominately
swiftly fiscally pitilessly ...

RBR: adverb, comparative

further gloomier grander graver greater grimmer harder harsher
healthier heavier higher however larger later leaner lengthier less-
perfectly lesser lonelier longer louder lower more ...

RBS: adverb, superlative

best biggest bluntest earliest farthest first furthest hardest
heartiest highest largest least less most nearest second tightest worst

RP: particle

aboard about across along apart around aside at away back before behind
by crop down ever fast for forth from go high i.e. in into just later
low more off on open out over per pie raising start teeth that through
under unto up up-pp upon whole with you

TO: "to" as preposition or infinitive marker

to

UH: interjection

Goodbye Goody Gosh Wow Jeepers Jee-sus Hubba Hey Kee-reist Oops amen
huh howdy uh dammit whammo shucks heck anyways whodunnit honey golly
man baby diddle hush sonuvabitch ...

VB: verb, base form

ask assemble assess assign assume atone attention avoid bake balkanize
bank begin behold believe bend benefit bevel beware bless boil bomb
boost brace break bring broil brush build ...

VBD: verb, past tense

dipped pleaded swiped regummed soaked tidied convened halted registered
cushioned exacted snubbed strode aimed adopted belied figgered
speculated wore appreciated contemplated ...

VBG: verb, present participle or gerund

telegraphing stirring focusing angering judging stalling lactating
hankerin' alleging veering capping approaching traveling besieging
encrypting interrupting erasing wincing ...

VBN: verb, past participle

multihulled dilapidated aerosolized chaired languished panelized used
experimented flourished imitated reunifed factored condensed sheared
unsettled primed dubbed desired ...

VBP: verb, present tense, not 3rd person singular

predominate wrap resort sue twist spill cure lengthen brush terminate
appear tend stray glisten obtain comprise detest tease attract
emphasize mold postpone sever return wag ...

VBZ: verb, present tense, 3rd person singular

bases reconstructs marks mixes displeases seals carps weaves snatches
slumps stretches authorizes smolders pictures emerges stockpiles
seduces fizzes uses bolsters slaps speaks pleads ...

WDT: WH-determiner

that what whatever which whichever

WP: WH-pronoun

that what whatever whatsoever which who whom whosoever

WRB: Wh-adverb

how however whence whenever where whereby whereever wherein whereof why

"""

# tag filter
def tag_filter(list_of_words):
    allowed_tags = ['CC','DT','IN','JJ','JJR','JJS','MD','NN','NNP','NNS','PDT','RB','RBR','RBS','RP','VB','VBD','VBG','VBN','VBP','VBZ','']
    tags = nltk.pos_tag(list_of_words)
    res = []
    l = len(list_of_words)
    for i in range(l):
        if tags[i][1] in allowed_tags:
            res.append(tags[i])
    return res

def preprocess(filename):
    fobj = open(fd_path+'/'+filename,'r')
    summary = eval(fobj.readline())
    ratings = eval(fobj.readline())
    reviews = eval(fobj.readline())
    fobj.close()
    no_of_reviews = len(ratings)
    mobile_corpus = []
    for i in range(no_of_reviews):
        label = get_label(ratings[i])
        review = reviews[i]
        mobile_corpus.append([tag_filter(remove_stop_words(extra_ascii_removal(word_tokenization(review)))),label])

    # finally putting up everything into file
    robj = open(rd_path+'/'+filename,'w')
    robj.write(str(mobile_corpus))
    robj.close()

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
