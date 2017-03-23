"""
This script read the output files from Filtered_Dataset
and perform preprocessing to this data

Thursday 23 March 2017 10:34:17 AM IST

"""

import os
import nltk
import ast

if __name__ == "__main__":

    files = os.listdir('../../Filtered_Dataset/')

    # for testing purpose
    file_obj = open('../../Filtered_Dataset/'+files[1],'r')
    summaries = ast.literal_eval(file_obj.readline())
    ratings = ast.literal_eval(file_obj.readline())
    reviews = ast.literal_eval(file_obj.readline())

    for i in range(len(reviews)):
        print "%d : %s\n"%(i+1,reviews[i])

    file_obj.close()
