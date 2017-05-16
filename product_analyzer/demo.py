import textblob as TextBlob as TB
import os

# returns a dictionary of indices
# dict = {
#   "-1" : [...],
#    "0" : [...],
#    "1" : [...]
# }
def sentiment_classifier(reviews,no_of_reviews):
    d = {
        -1 : [],
        0 : [],
        1 : []
    }
    for i in range(no_of_reviews):
        tb = TB(reviews[i])
        st = tb.sentiment
        if st[0] >= 0.10:
            d[1].append(i)
        elif st[0] <= -0.10:
            d[-1].append(i)
        else:
            d[0].append(i)
    return d


if __name__ == "__main__":

    path = "../../Filtered_Dataset"

    filenames = os.listdir(path)
    l = len(filenames)

    for i in xrange(l):

        fobj = open(filenames[i],'r')

        summary = eval(fobj.readline())
        ratings = eval(fobj.readline())
        reviews = eval(fobj.readline())

        fobj.close()
