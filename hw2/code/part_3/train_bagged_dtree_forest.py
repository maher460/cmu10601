import json 
import dtree
import jsonpickle
import random

DEBUG = True


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
	bagged_dtree_forest = []
	for i in range(100):
		print("About to start processing tree: " + str(i) + " ...")
		subdata = random.sample(traindata, int(0.1 * len(traindata)))
		if DEBUG:
			print("size of subdata: " + str(len(subdata)))
		subdata_attr_lab = separate(subdata)
		dtree_temp = dtree.Dtree(subdata_attr_lab[0], subdata_attr_lab[1])
		bagged_dtree_forest.append(dtree_temp)
	return bagged_dtree_forest


# MAIN

print("Loading processed train data...")
traindata_processed_file = open("../processed_data/intrusion.traindataprocessed", "r")
traindata = json.loads(traindata_processed_file.read())
traindata_processed_file.close()
print("Done loading processed train data")

bagged_dtree_forest = train_forest(traindata)

if DEBUG:
	print("Number of trees in bagged_dtree_forest: " + str(len(bagged_dtree_forest)))

print("Writing bagged_dtree_forest to file...")
traindata_processed_file = open("processed_trees/intrusion.baggeddtreeforest", "w")
traindata_processed_file.write(jsonpickle.encode(bagged_dtree_forest))
traindata_processed_file.close()
print("Done writing bagged_dtree_forest to file")