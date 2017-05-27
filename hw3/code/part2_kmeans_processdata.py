import math
import json
import random
import numpy as np
import multiprocessing

NUM_CENTROIDS = 256

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

def map_mean_function(x):
	y = np.array(x)
	#y = x
	if(y.size > 0):
		return np.mean(x, axis=0)
	else:
		return np.array([])

#Features

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


# Get continuous and non-continuous

continuous = []
not_continuous = []

for idx, item in enumerate(features):
	if "continuous" in item[1]:
		continuous.append(idx)
	else:
		not_continuous.append(idx)




traindata_file = open("data/intrusion.traindata", "r")
traindata_str = traindata_file.read()
traindata = traindata_str.split("\n")

traindata_continuous = []
traindata_discrete = []
td_len = len(traindata)

print("Reading traindata from file...")
for idx, item in enumerate(traindata):
	item = item.split(",")
	item[-1] = item[-1][:-1]
	traindata[idx] = item

	if(idx < td_len - 1):
		c = [float(item[index]) for index in continuous]
		d = [item[index] for index in not_continuous]
		d.append(item[-1])
		traindata_continuous.append(c)
		traindata_discrete.append(d)


	if(idx % 10000 == 0):
		print("Done reading " + str(idx) + " traindata")
traindata = traindata[:-1]
#traindata_continuous = traindata_continuous[:-1]
#print(traindata)

print("size of traindata: ", len(traindata))
print("size of traindata_continous: ", len(traindata_continuous))
print("size of traindata_discrete: ", len(traindata_discrete))
num_inst = len(traindata_continuous)
num_cattr = len(continuous)
num_dattr = len(not_continuous)

traindata_file.close()


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


print("converting to numpy matrix....")
cTraindata = np.array(traindata_continuous)

# print("removing not conituous columns....")
# cTraindata = np.delete(traindata_np, not_continuous, 1)

#cTraindata = cTraindata.astype('float32')

print("calculating the mean for each column....")
all_mean = np.mean(cTraindata, axis=0)
#print("all_mean: ", all_mean)

print("calculating the std for each column....")
all_std = np.std(cTraindata, axis=0)
#print("all_std", all_std)


# Normalizing

#print(cTraindata)

print("all_mean.size", all_mean.size)
print("num_inst", num_inst)
count_updates = 0;
for i in range(num_inst):
	count_updates += 1
	for j in range(num_cattr):
		#pass
		#print("~~~~~")
		#print(cTraindata[i,j])
		if(all_std[j] == 0):
			cTraindata[i,j] = 0.0
		else:
			cTraindata[i,j] = (cTraindata[i,j] - all_mean[j]) / all_std[j]
		#print(cTraindata[i,j])
	if(count_updates % 10000 == 0):
		print("Done updating " + str(count_updates) + " traindata")


print("Loading kmeans centroids...")
traindata_processed_file = open("processed_data/intrusion.kmeanspartialcentroids", "r")
centroids = json.loads(traindata_processed_file.read())

#print(traindata)
traindata_processed_file.close()

print("Done loading centroids...")

print("About to convert centroids into numpy centroids....")
centroids = np.array(centroids)
print("Done converting centroids into numpy centroids....")



# assignments_count = 0
# for i in range(num_inst):
# 	assignments_count += 1;

# 	min_dist = float('infinity')
# 	min_id = -1

# 	for j in range(NUM_CENTROIDS):
		
# 		dist = np.linalg.norm(cTraindata[i]-centroids[j])

# 		if(dist < min_dist):
# 			min_id = j
# 			min_dist = dist

# 	assignments[min_id].append(cTraindata[i])
# 	new_error += min_dist

# 	if(assignments_count % 10000 == 0):
# 		print(">>>>>>>>>> Done assigning " + str(assignments_count) + " traindata")




print("processing traindata...")
for idx, item in enumerate(traindata_discrete):
	# for k in continuous.keys():
	# 	# if(continuous[k][1]-continuous[k][0] > 0):
	# 	# 	item[k] = int(math.floor((10 * (float(item[k]) - continuous[k][0])) / (continuous[k][1] - continuous[k][0])))
	# 	# else:
	# 	# 	item[k]= int(float(item[k]))
	# 	item[k] = centroids[k][assignments[k][idx]]

	#c_item = cTraindata[idx]

	min_dist = float('infinity')
	min_id = -1

	for j in range(NUM_CENTROIDS):
		
		dist = np.linalg.norm(cTraindata[idx]-centroids[j])

		if(dist < min_dist):
			min_id = j
			min_dist = dist


	item[-1] = attacktypes_map[item[-1]]
	traindata_discrete[idx] = item[:-1] + [min_id] + [item[-1]]
	if(idx % 10000 == 0):
		print("Done processing " + str(idx) + " traindata")

#print(traindata)

print("writing processed traindata to file...")
traindata_processed_file = open("processed_data/intrusion.kmeanstraindataprocessed", "w")
traindata_processed_file.write(json.dumps(traindata_discrete))
traindata_processed_file.close()
print("Done writing processed traindata to file")

# traindata_processed_file = open("intrusion_small.traindataprocessed", "r")
# traindata2 = json.loads(traindata_processed_file.read())
# print("TRAINDATA2\n")
# print(traindata2)
# traindata_processed_file.close()





