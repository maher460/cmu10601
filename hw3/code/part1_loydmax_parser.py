import math
import json
import random

THRESHOLD = 1

def segregate(attributearray, value):
    outlist = []
    for i in range(0, len(attributearray)):
        if(attributearray[i] == value):
            outlist.append(i)
    return outlist

def select_labels(labels, ids):
    result = []
    for i in ids:
        result.append(labels[i])
    return result

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
		continuous[idx] = []

#print(continuous) 

print("calculating min and max...")
count = 0
for d in traindata:
	for k in continuous.keys():
		continuous[k].append(float(d[k]))
	if(count % 10000 == 0):
		print("Done adding to continuous " + str(count) + " instances")
	count = count + 1
#print(continuous)

centroids = {}
val_errors = {}


for k in continuous.keys():
	centroids[k] = random.sample(continuous[k], 10)
	val_errors[k] = 0

running = True

loyd_count = 0

while(running):

	print("Loyd Count: ", loyd_count)
	print(centroids)
	loyd_count += 1;
	running = False
	assignments = {}
	new_centroids = {}
	new_val_errors = {}

	for k in continuous.keys():
		new_centroids[k] = []
		assignments[k] = []
		new_val_errors[k] = 0
		for c in continuous[k]:
			min_dist = float('infinity')
			min_id = -1
			for p in range(len(centroids[k])):
				dif = centroids[k][p] - c
				if dif < 0:
					dif = (-1 * dif)
				if(dif < min_dist):
					min_dist = dif
					min_id = p 
			assignments[k].append(min_id) #changed from p to min_id

		for p in range(len(centroids[k])):
			temp = select_labels(continuous[k], segregate(assignments[k], p))
			if(len(temp) > 0):
				new_centroids[k].append(sum(temp)/float(len(temp)))
			else:
				#new_centroids[k].append(random.sample(continuous[k], 1)[0])
				new_centroids[k].append(centroids[k][p])

		for i in range(len(continuous[k])):
			x_val = continuous[k][i]
			centroid_x_val = new_centroids[k][assignments[k][i]]
			diff_sq = (x_val - centroid_x_val) * (x_val - centroid_x_val)
			new_val_errors[k] = new_val_errors[k] + diff_sq

		val_change = math.fabs(new_val_errors[k] - float(val_errors[k])) / (float(new_val_errors[k] + val_errors[k] + 1)/2) * 100
		
		print("new_val_error: ", new_val_errors[k])
		print("val_error: ", val_errors[k])
		print("val_change: ", val_change)
		
		if (val_change > THRESHOLD):
			running = True

		for p in range(len(centroids[k])):
			centroids[k][p] = new_centroids[k][p]

		val_errors[k] = new_val_errors[k]



		# for p in range(len(centroids[k])):
		# 	difff = (math.fabs(centroids[k][p]-float(new_centroids[k][p]))/(float(centroids[k][p] + new_centroids[k][p] + 1 )/2)*100)
		# 	print(centroids[k][p])
		# 	print(new_centroids[k][p])
		# 	print("difff: ", difff)
		# 	if( difff > THRESHOLD ):
		# 		running = True
		# 	centroids[k][p] = new_centroids[k][p]
	print(centroids)



print("processing traindata...")
for idx, item in enumerate(traindata):
	for k in continuous.keys():
		# if(continuous[k][1]-continuous[k][0] > 0):
		# 	item[k] = int(math.floor((10 * (float(item[k]) - continuous[k][0])) / (continuous[k][1] - continuous[k][0])))
		# else:
		# 	item[k]= int(float(item[k]))
		item[k] = centroids[k][assignments[k][idx]]
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





