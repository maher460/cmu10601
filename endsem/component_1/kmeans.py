import math
import json
import random
import numpy as np
import multiprocessing

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

def map_mean_function(x):
	y = np.array(x)
	#y = x
	if(y.size > 0):
		return np.mean(x, axis=0)
	else:
		return np.array([])

def do_kmeans(traindata_continuous, NUM_CENTROIDS=32):

	num_inst = len(traindata_continuous)

	try:
		num_cattr = len(traindata_continuous[0])
	except Exception as e:
		print e
		raise

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

	#print(cTraindata)


	centroids = cTraindata[:NUM_CENTROIDS]
	#print("starting centroids: ", centroids)
	old_error = 0.0

	running = True
	kmeans_count = 0

	while(running):
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		print("------------------------------------------------------")
		print(">>> Kmeans Iteration: ", kmeans_count)
		kmeans_count += 1;

		running = False
		new_centroids = []
		assignments = [[] for i in range(NUM_CENTROIDS)]
		new_error = 0.0

		assignments_count = 0
		for i in range(num_inst):
			assignments_count += 1;

			min_dist = float('infinity')
			min_id = -1

			for j in range(NUM_CENTROIDS):
				
				dist = np.linalg.norm(cTraindata[i]-centroids[j])

				if(dist < min_dist):
					min_id = j
					min_dist = dist

			assignments[min_id].append(cTraindata[i])
			new_error += min_dist

			if(assignments_count % 10000 == 0):
				print(">>>>>>>>>> Done assigning " + str(assignments_count) + " traindata")

		#print(assignments)

		print(">>>>> About to map mean...")
		pool = multiprocessing.Pool()
		new_centroids = pool.map(map_mean_function, assignments)
		#print(new_centroids)
		pool.close()

		print(">>>>> Done with parallel map mean....")

		for j in range(NUM_CENTROIDS):
			if((new_centroids[j] != []) or (new_centroids[j].size > 0 )):
				centroids[j] = new_centroids[j]

		val_change = (math.fabs(new_error - old_error) / ((new_error + old_error + 1)/2)) * 100
			
		print("new_error: ", new_error)
		print("old_error: ", old_error)
		print("val_change: ", val_change)
		
		if (val_change > THRESHOLD):
			running = True

		old_error = new_error

		print("writing partial centroids to file...")
		traindata_processed_file = open("parsed_data/data1.kmeanspartialcentroids", "w")
		traindata_processed_file.write(json.dumps(centroids.tolist()))
		traindata_processed_file.close()
		print("Done writing partial centroids to file")

	print(centroids)
	return centroids
