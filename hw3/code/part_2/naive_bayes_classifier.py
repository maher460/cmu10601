import json 
import jsonpickle

DEBUG = False 
SMOOTH_E = 0.1

# Segregating out instances that take a particular value
# attributearray is an N x 1 array.
def segregate(attributearray, value):
    outlist = []
    for i in range(0, len(attributearray)):
        if(attributearray[i] == value):
            outlist.append(i)
    return outlist

def unique_labels(labels):
    unique_labels = []
    for e in labels:
        if (e not in unique_labels):
            unique_labels.append(e)
    return unique_labels


def select_labels(labels, ids):
    result = []
    for i in ids:
        result.append(labels[i])
    return result

def transpose(matrix):
    if(len(matrix) < 1):
        return matrix
    else:
        new_matrix = []
        for k in range(len(matrix[0])):
            new_matrix.append([])
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                new_matrix[j].append(matrix[i][j])

            if DEBUG:
                if(i % 1000 == 0):
                    print("transposing " + str(i) + " ....")
        return new_matrix


print("Loading processed train data...")
traindata_processed_file = open("../processed_data/intrusion.kmeanstraindataprocessed", "r")
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

attributes_tx = transpose(attributes)

values_set_attrs = []

for i in range(len(attributes_tx)):
	values_set_attrs.append(unique_labels(attributes_tx[i]))


print("Reading attacktypes from file...")
attacktypes_file = open("../data/attacktypes.list", "r")
attacktypes_str = attacktypes_file.read()
attacktypes = attacktypes_str.split("\n")
attacktypes = attacktypes[:-1]

attacktypes_set = []
for idx, item in enumerate(attacktypes):
	item = item.split(" ")
	if item[1] not in attacktypes_set:
		attacktypes_set.append(item[1])
	attacktypes[idx] = item

attacktypes_file.close()


# features_file = open("../data/intrusion.features", "r")
# features_str = features_file.read()
# features = features_str.split("\n")

# print("Reading features from file...")
# for idx, item in enumerate(features):
# 	item = item.split(": ")
# 	item[-1] = item[-1][:-1]
# 	features[idx] = item

# features = features[:-1]
# #print(features)

# features_file.close()

# continuous = []

# for idx, item in enumerate(features):
# 	if "continuous" in item[1]:
# 		continuous.append(idx)



# seg_by_class = {}
# seg_by_class2 = {}
# prob_class = {}

# for e in attacktypes_set:
# 	seg_by_class[e] = select_labels(attributes, segregate(labels, e))

# for k in seg_by_class.keys():
# 	temp_list = seg_by_class[k]

# 	prob_class[str(k)] = ((len(temp_list) * 1.0) + SMOOTH_E) / (len(labels) + SMOOTH_E)

# 	attributes_t = transpose(temp_list)
# 	new_list = []
# 	for i in range(len(attributes_t)):
# 		temp_dict = {}
# 		num_total = len(attributes_t[i])

# 		values_set_attrs2 = values_set_attrs[i]
# 		if(i in continuous):
# 			values_set_attrs2 = range(11)
# 		for v in values_set_attrs2:
# 			num_v = len(segregate(attributes_t[i], v))
# 			temp_dict[str(v)] = ((num_v * 1.0) + SMOOTH_E) / (num_total + (SMOOTH_E * len(values_set_attrs2)))
# 		if(i == 20 and len(values_set_attrs2) == 1 and str(values_set_attrs2[0]) == "0"):
# 			temp_dict[str(1)] = SMOOTH_E / (num_total + SMOOTH_E)
# 		new_list.append(temp_dict)
# 	seg_by_class2[str(k)] = new_list


seg_by_class = {}
seg_by_class2 = {}
class_count = {}
class_attr_count = {}

for e in attacktypes_set:
	seg_by_class[e] = select_labels(attributes, segregate(labels, e))

for k in seg_by_class.keys():
	temp_list = seg_by_class[k]

	class_count[str(k)] = len(temp_list)

	attributes_t = transpose(temp_list)
	new_list = []

	class_attr_count[k] = []

	for i in range(len(attributes_t)):
		temp_dict = {}
		class_attr_count[k].append(len(attributes_t[i]))

		values_set_attrs2 = unique_labels(attributes_t[i])

		for v in values_set_attrs2:
			num_v = len(segregate(attributes_t[i], v))
			temp_dict[str(v)] = num_v
		# if(i == 20 and len(values_set_attrs2) == 1 and str(values_set_attrs2[0]) == "0"):
		# 	temp_dict[str(1)] = SMOOTH_E / (num_total + SMOOTH_E)
		new_list.append(temp_dict)
	seg_by_class2[str(k)] = new_list


result = [seg_by_class2, class_attr_count, class_count, len(labels)]

print("Writing trained naive bayes classification to file...")
traindata_processed_file = open("processed_classifier/intrusion.trainedclassifier", "w")
traindata_processed_file.write(jsonpickle.encode(result))
traindata_processed_file.close()
print("Done writing naive bayes classification to file")


