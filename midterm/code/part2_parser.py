# This is a parser for the midterm data
# Author: Maher Khan

import json

traindata_file = open("data/midtermdata/midterm.train", "r")
traindata_str = traindata_file.read()
traindata = traindata_str.split("\n")
traindata_file.close()

print("Reading traindata from file...")
for idx, item in enumerate(traindata):
	item = item.split("\t")
	#item[-1] = item[-1][:-1]
	traindata[idx] = item
	if(idx % 1 == 0):
		print("Done reading " + str(idx) + " traindata")
traindata = traindata[:-1]
print(len(traindata))

traindata_header = traindata[0]
traindata = traindata[1:]


print("writing processed traindata to file...")
traindata_processed_file = open("processed_data/midtermdata/midterm.traindataprocessed", "w")
traindata_processed_file.write(json.dumps([traindata_header, traindata]))
traindata_processed_file.close()
print("Done writing processed traindata to file")

print(traindata_header)
print(traindata)

traindata_file = open("data/midtermdata/midterm.test", "r")
traindata_str = traindata_file.read()
traindata = traindata_str.split("\n")
traindata_file.close()

print("Reading traindata from file...")
for idx, item in enumerate(traindata):
	item = item.split("\t")
	#item[-1] = item[-1][:-1]
	traindata[idx] = item
	if(idx % 100 == 0):
		print("Done reading " + str(idx) + " traindata")
traindata = traindata[:-1]
print(len(traindata))

traindata_header = traindata[0]
traindata = traindata[1:]

print("writing processed traindata to file...")
traindata_processed_file = open("processed_data/midtermdata/midterm.testdataprocessed", "w")
traindata_processed_file.write(json.dumps([traindata_header, traindata]))
traindata_processed_file.close()
print("Done writing processed traindata to file")