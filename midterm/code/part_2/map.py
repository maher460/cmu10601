import mle
import json
import math
import jsonpickle

DEBUG = False

def segregate(attributearray, value):
    outlist = []
    for i in range(0, len(attributearray)):
        if(attributearray[i] == value):
            outlist.append(i)
    return outlist

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

            # if DEBUG:
            #     if(i % 1000 == 0):
            #         print("transposing " + str(i) + " ....")
        return new_matrix


def loadDAGs(dags_str):
    print("About to load dtree")
    traindata_processed_file = open(dags_str, "r")
    trained_dtree = jsonpickle.decode(traindata_processed_file.read())
    traindata_processed_file.close()
    print("trained dtree loaded")
    return trained_dtree

traindata_processed_file = open("../processed_data/midtermdata/midterm.traindataprocessed", "r")
traindata = json.loads(traindata_processed_file.read())
traindata_header = traindata[0]
traindata = traindata[1]

#print(traindata)
traindata_processed_file.close()

print("Done loading processed train data")



all_combs_probs = mle.all_comb_probs(range(len(traindata_header)), traindata)
print(all_combs_probs)
if DEBUG:
    for k in all_combs_probs.keys():
        #print(k, all_combs_probs[k])
        if(int(all_combs_probs[k] * 1000000) == 0):
            print(k, all_combs_probs[k])

all_dags = loadDAGs("processed_stuff/all_dags")

all_log_likelihood = []

for g in all_dags:
    sum_log_probs = 0.0
    pars_g = transpose(g)
    lambda_count = 0
    for i in range(5):
        child = i
        pars = segregate(pars_g[child], 1)
        lambda_count = lambda_count + (2**(len(pars) + 1))
    # if DEBUG:
    #     #print(g)
    #     #print(pars_g)
    #     print(lambda_count)

    for t in traindata:
        for i in range(5):
            child = i
            pars = segregate(pars_g[child], 1)
            val_list = []
            val_list.append((child, t[child]))
            for p in pars:
                val_list.append((p, t[p]))
            val_tuple = tuple(val_list)
            # if DEBUG:
            #     if(int(all_combs_probs[val_tuple] * 1000000) == 0):
            #         print(val_tuple, all_combs_probs[val_tuple])
            sum_log_probs = sum_log_probs + math.log(all_combs_probs[val_tuple])
    sum_log_probs = sum_log_probs - (2 * lambda_count)
    all_log_likelihood.append(sum_log_probs)

cur_max = float('-inf');
cur_max_idx = None;

for i in range(len(all_log_likelihood)):
    if(all_log_likelihood[i] > cur_max):
        cur_max = all_log_likelihood[i]
        cur_max_idx = i

print("graph id: ", cur_max_idx)
print("log likelihood: ", all_log_likelihood[cur_max_idx])
print("graph: ", all_dags[cur_max_idx])
#print(all_log_likelihood)

print("Writing bayes_net and all_combs_probs to file...")
traindata_processed_file = open("processed_stuff/bayes_net", "w")
traindata_processed_file.write(jsonpickle.encode([all_dags[cur_max_idx], all_combs_probs]))
traindata_processed_file.close()
print("Done writing bayes_net and all_combs_probs to file")

        



