import math
import json

traindata_file = open("data/intrusion.traindata", "r")
traindata_str = traindata_file.read()
traindata = traindata_str.split("\n")

print("Reading traindata from file...")
for idx, item in enumerate(traindata):
	item = item.split(",")
	item[-1] = item[-1][:-1]
	traindata[idx] = item
	if(idx % 10000 == 0):
		print("Done reading " + str(idx) + " traindata")
traindata = traindata[:-1]
#print(traindata)

traindata_file.close()

features_file = open("data/intrusion.features", "r")
features_str = features_file.read()
features = features_str.split("\n")

print("Reading features from file...")
for idx, item in enumerate(features):
	item = item.split(": ")
	item[-1] = item[-1][:-1]
	features[idx] = item

features = features[:-1]
#print(features)

features_file.close()

print("Reading attacktypes from file...")
attacktypes_file = open("data/attacktypes.list", "r")
attacktypes_str = attacktypes_file.read()
attacktypes = attacktypes_str.split("\n")
attacktypes = attacktypes[:-1]

attacktypes_map = {}
for idx, item in enumerate(attacktypes):
	item = item.split(" ")
	attacktypes_map[item[0]] = item[1]
	attacktypes[idx] = item

#print(attacktypes)
#print(attacktypes_map)

attacktypes_file.close()

continuous = {}

for idx, item in enumerate(features):
	if "continuous" in item[1]:
		continuous[idx] = [float('inf'), float('-inf')]

#print(continuous) 

print("calculating min and max...")
count = 0
for d in traindata:
	for k in continuous.keys():
		if float(d[k]) < continuous[k][0]:
			continuous[k][0] = float(d[k])
		if float(d[k]) > continuous[k][1]:
			continuous[k][1] = float(d[k])
	if(count % 10000 == 0):
		print("Done calculating min max of " + str(count) + " instances")
	count = count + 1

print(continuous)

print("processing traindata...")
for idx, item in enumerate(traindata):
	for k in continuous.keys():
		if(continuous[k][1]-continuous[k][0] > 0):
			item[k] = int(math.floor((10 * (float(item[k]) - continuous[k][0])) / (continuous[k][1] - continuous[k][0])))
		else:
			item[k]= int(float(item[k]))
	item[-1] = attacktypes_map[item[-1]]
	traindata[idx] = item
	if(idx % 10000 == 0):
		print("Done processing " + str(idx) + " traindata")

#print(traindata)

print("writing processed traindata to file...")
traindata_processed_file = open("processed_data/intrusion.traindataprocessed", "w")
traindata_processed_file.write(json.dumps(traindata))
traindata_processed_file.close()
print("Done writing processed traindata to file")

# traindata_processed_file = open("intrusion_small.traindataprocessed", "r")
# traindata2 = json.loads(traindata_processed_file.read())
# print("TRAINDATA2\n")
# print(traindata2)
# traindata_processed_file.close()




