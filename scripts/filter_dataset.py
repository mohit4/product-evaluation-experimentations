"""

This script inputs the dataset as compressed .tar.gz file and adds it to the directory with
understandable format.


Friday 17 March 2017 09:19:14 AM IST

"""
import os
import sys
import gzip

def parse(path):
	g = gzip.open(path,'r')
	for l in g:
		yield eval(l)

if __name__ == "__main__":
	count = 0
	if len(sys.argv) >= 2:
		# get the fileName
		dataset_path = sys.argv[1]
		# check for existence of the fileName given as command line argument
		if os.path.exists(dataset_path):
			# extract the firstName of the dataset only
			dirName = "Filtered_Dataset"
			# check for its existence
			if not os.path.isdir(dirName):
				os.mkdir(dirName)
			ratings = []
			reviewTexts = []
			summaries = []

			data_gen = parse(dataset_path)

			try:
				one_object = data_gen.next()
				product_id = one_object['asin']
				ratings = [one_object['overall']]
				reviewTexts = [one_object['reviewText']]
				summaries = [one_object['summary']]
				while True:
					one_object = data_gen.next()
					if one_object['asin'] == product_id:
						ratings.append(one_object['overall'])
						reviewTexts.append(one_object['reviewText'])
						summaries.append(one_object['summary'])
					else:
						print "Working on ... ",product_id
						count += 1
						# write all the contents into files
						if not os.path.isdir(dirName+'/'+product_id):
							os.mkdir(dirName+'/'+product_id)
						# opening the file in append mode will handle they case if file in not present
						file1 = open(dirName+'/'+product_id+'/'+'ratings.txt','a')
						file1.write(str(ratings))
						file1.close()

						file2 = open(dirName+'/'+product_id+'/'+'reviewTexts.txt','a')
						file2.write(str(reviewTexts))
						file2.close()

						file3 = open(dirName+'/'+product_id+'/'+'summaries.txt','a')
						file3.write(str(summaries))
						file3.close()

						# reset the current buffers and set id to current id
						ratings, reviewTexts, summaries = [],[],[]
						product_id = one_object['asin']
			except StopIteration:
				# last values will still be in buffers

				print "Working on ... ",product_id
				count += 1

				if not os.path.isdir(dirName+'/'+product_id):
					os.mkdir(dirName+'/'+product_id)

				file1 = open(dirName+'/'+product_id+'/'+'ratings.txt','a')
				file1.write(str(ratings))
				file1.close()

				file2 = open(dirName+'/'+product_id+'/'+'reviewTexts.txt','a')
				file2.write(str(reviewTexts))
				file2.close()

				file3 = open(dirName+'/'+product_id+'/'+'summaries.txt','a')
				file3.write(str(summaries))
				file3.close()

		else:
			print "Couldn't find the dataset!"

		print "Done!"
		print "Total products :",count
