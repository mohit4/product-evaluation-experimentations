"""
Demo for textblob sentiment analyzer (internally uses Naive Bayes Algorithm)
"""

from textblob import TextBlob
import os
import sys

def review_analyze(review):
    test = TextBlob(review)
    polarity = test.sentiment.polarity
    if polarity >= 0.1:
        return ('pos',polarity)
    elif polarity <= -0.1:
        return ('neg',polarity)
    return ('neu',polarity)

def process_file(fileName):
    path = "../../Filtered_Dataset"
    f = open(path+'/'+fileName,'r')
    summaries = eval(f.readline())
    ratings = eval(f.readline())
    reviews = eval(f.readline())
    no_of_reviews = len(ratings)

    # list contains ids of reviews
    neg_reviews = []
    pos_reviews = []
    neu_reviews = []

    for i in range(no_of_reviews):
        (pol,val) = review_analyze(reviews[i])
        if pol == 'pos':
            pos_reviews.append((i,val))
        elif pol == 'neg':
            neg_reviews.append((i,val))
        else:
            neu_reviews.append((i,val))

    print "Product id :",fileName
    print "Pos :",len(pos_reviews)
    print "Neg :",len(neg_reviews)
    print "Neu :",len(neu_reviews)
    print "---"*10

if __name__ == "__main__":
    path = "../../Filtered_Dataset"
    if not os.path.isdir(path):
        print "Dataset not filtered! Please filter the dataset to continue."
        sys.exit(1)

    no_of_files = 100
    fileNames = os.listdir(path)[:no_of_files]
    for fileName in fileNames:
        process_file(fileName)
