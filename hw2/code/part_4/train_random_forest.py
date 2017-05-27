import json 
import dtree_rf
import jsonpickle
import random

DEBUG = False


def separate(traindata):
	attributes = []
	labels = []

	for i in range(len(traindata)):
		attributes.append(traindata[i][:-1])
		labels.append(traindata[i][-1])

		if DEBUG:
			if(i % 10000 == 0):
				print("separated " + str(i) + " traindata into attributess and labels...")

	return [attributes, labels]



def train_forest(traindata):
	random_forest = []
	for i in range(100):
		print("About to start processing tree: " + str(i) + " ...")
		subdata = traindata
		if DEBUG:
			print("size of subdata: " + str(len(subdata)))
		subdata_attr_lab = separate(subdata)
		dtree_temp = dtree_rf.Dtree(subdata_attr_lab[0], subdata_attr_lab[1])
		random_forest.append(dtree_temp)
	return random_forest


# MAIN

print("Loading processed train data...")
traindata_processed_file = open("../processed_data/intrusion.traindataprocessed", "r")
traindata = json.loads(traindata_processed_file.read())
traindata_processed_file.close()
print("Done loading processed train data")

random_forest = train_forest(traindata)

if DEBUG:
	print("Number of trees in random_forest: " + str(len(random_forest)))

print("Writing random_forest to file...")
traindata_processed_file = open("processed_trees/intrusion.randomforest", "w")
traindata_processed_file.write(jsonpickle.encode(random_forest))
traindata_processed_file.close()
print("Done writing random_forest to file")