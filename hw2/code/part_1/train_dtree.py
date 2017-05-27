import json 
import dtree
import jsonpickle

print("Loading processed train data...")
traindata_processed_file = open("../processed_data/intrusion.traindataprocessed", "r")
traindata = json.loads(traindata_processed_file.read())

#print(traindata)
traindata_processed_file.close()

print("Done loading processed train data")

attributes = []
labels = []

for i in range(len(traindata)):
	attributes.append(traindata[i][:-1])
	labels.append(traindata[i][-1])
	if(i % 10000 == 0):
		print("separated " + str(i) + " traindata into attributess and labels...")

new_dtree = dtree.Dtree(attributes, labels)

print("Done making dtree!")

print("Writing trained dtree to file...")
traindata_processed_file = open("processed_trees/intrusion.traineddtree", "w")
traindata_processed_file.write(jsonpickle.encode(new_dtree))
traindata_processed_file.close()
print("Done writing trained dtree to file")