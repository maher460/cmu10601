import kmeans
import json
import numpy as np

NUM_GAUSSIANS = 32
DO_KMEANS = False
DEBUG = True

mixture_weights = [1.0/NUM_GAUSSIANS] * NUM_GAUSSIANS

if DEBUG:
    print ("mixture_weights: ", mixture_weights)

print("Loading parsed data...")
traindata_processed_file = open("parsed_data/data1.universalenrollparsed", "r")
data = json.loads(traindata_processed_file.read())
traindata_processed_file.close()
print("Done loading parsed data!")

means = []
if DO_KMEANS:
    means = kmeans.do_kmeans(data, 32)
else:
    print("Loading centroids...")
    traindata_processed_file = open("parsed_data/data1.kmeanspartialcentroids", 
                                    "r")
    means = json.loads(traindata_processed_file.read())
    traindata_processed_file.close()
    print("Done loading centroids!")

data_np = np.array(data)

variances_np = np.var(data_np, axis=0)

if DEBUG:
    print ("variances_np: ", variances_np)

variances = [variances_np.tolist()] * NUM_GAUSSIANS

initial_params = {
                      'mixture_weights': mixture_weights,
                      'means': means,
                      'variances': variances
                  }

print("writing inital parameters to file...")
traindata_processed_file = open("parsed_data/data1.initialparameters", "w")
traindata_processed_file.write(json.dumps(initial_params))
traindata_processed_file.close()
print("Done writing inital parameters to file")
