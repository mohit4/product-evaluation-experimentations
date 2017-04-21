"""
Script to work upon the filtered dataset and extract a labelled dataset from it
using TextBlob sentiment analyzer

pre-script : filter_dataset.py

Note to self : Prefer using yield wherever neccessary,
    will drastically reduce the space complexity.
    Alternatively use pandas module

"""

from textblob import TextBlob   # to handle the labelling
import os   # listing directories and files
import sys  # mainly for system exit command
import timeit   # to calculate the time taken

dataset_path = "../../Filtered_Dataset/"
result_path = "../../Labelled_Dataset/"

# toggle debugging from here
debugging = False

# the review analyzer only identifies the review as positive or negative
def review_analyze(review):
    test = TextBlob(review)
    pol = test.sentiment.polarity
    if pol > 0:
        return ('pos',pol)
    return ('neg',pol)

# for processing and generating the result files
def process_file(fileName):
    src_obj = open(dataset_path+fileName,'r')    # source file
    src_obj.readline() # summary
    src_obj.readline() # ratings
    text_reviews = eval(src_obj.readline())
    src_obj.close()

    # a single file multiple reviews
    # processed reviews will be stored as a
    # list of dict
    single_file_labels = []

    pos, neg = 0,0

    for one_review in text_reviews:
        values = review_analyze(one_review)
        # single dict format
        one_dict = {"review":one_review,"label":values[0],"polarity":values[1]}
        if values[0]=='pos':
            pos+=1
        else:
            neg+=1
        single_file_labels.append(one_dict)
        if debugging:
            print "review   :",one_dict["review"]
            print "label    :",one_dict["label"]
            print "polarity :",one_dict["polarity"]
            print "--------------------------------"
    res_obj = open(result_path+fileName,'w') # result file
    res_obj.write(str(single_file_labels))
    res_obj.close()
    return (pos,neg)

# if __name__ == "__main__":
# putting up the starting pointer
start = timeit.default_timer()

if debugging:
    print "filter_dataset path :",dataset_path

# checking for filtered dataset
if not os.path.isdir(dataset_path):
    print "Filtered Dataset not found! Please run filter_dataset.py"
    sys.exit()

# creating the result directory if not exists
if not os.path.isdir(result_path):
    os.mkdir(result_path)

# listing and processing fileNames
fileNames = os.listdir(dataset_path)
total_files = len(fileNames)
for i in range(total_files):
    res = process_file(fileNames[i])
    print "[ %3.2f %%] Processing...%s\t( pos %3d, neg %3d )"%(float((i+1)*100)/(total_files),fileNames[i],res[0],res[1])

# putting up the ending pointer
end = timeit.default_timer()

# finishing up
print "Total files worked upon :",len(fileNames)
print "time taken :",end-start,"sec(s)"
