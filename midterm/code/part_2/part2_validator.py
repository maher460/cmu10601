import jsonpickle
import json
import xlwings as xw
import math
import mle

DEBUG = False
SMOOTH_E = 0.1

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

traindata_processed_file = open("../processed_data/midtermdata/midterm.traindataprocessed", "r")
traindata = json.loads(traindata_processed_file.read())
traindata_header = traindata[0]
traindata = traindata[1]

#print(traindata)
traindata_processed_file.close()

print("Done loading processed train data")



all_combs_probs = mle.all_comb_probs(range(len(traindata_header)), traindata)

testdata_results_file = open("../data/midtermdata/midterm.testclass", "r")
testdata_results_str = testdata_results_file.read()
testdata_results = testdata_results_str.split("\n")
testdata_results = testdata_results[1:-1]



print("Loading processed test data")
testdata_processed_file = open("../processed_data/midtermdata/midterm.testdataprocessed", "r")
testdata = json.loads(testdata_processed_file.read())
testdata_processed_file.close()
print("TESTDATA loaded...")
testdata = testdata[1]

def loadClassifier(classifier_str):
    print("About to load dtree")
    traindata_processed_file = open(classifier_str, "r")
    trained_dtree = jsonpickle.decode(traindata_processed_file.read())
    traindata_processed_file.close()
    print("trained dtree loaded")
    return trained_dtree

def calc_and_save(tree_str, confusion_matrix, graph, offset):
    correct = 0
    attacktypes_set = ['Y','N']
    for e in ['Y','N']:
        correct = correct + confusion_matrix[e][e]

    print(((correct * 1.0) / len(testdata)) * 100)

    score = (((correct * 1.0) / len(testdata)) * 100)

    toWrite = ""
    toWrite += "Test result: " + str(score) + "/100\n\n"
    toWrite += "Selected DAG:\n"
    toWrite += "(0 means no edge from row_number to col_number)\n"
    toWrite += "(1 means there is an edge from row_number to col_number)\n\n"
    toWrite += "[\n"
    for i in range(len(graph)):
        toWrite += str(graph[i]) + "\n"
    toWrite += "]\n" 

    print("Writing test results to file...")
    traindata_processed_file = open("part2_results.txt", "w")
    #traindata_processed_file.write(jsonpickle.encode([all_dags[cur_max_idx], all_combs_probs]))
    traindata_processed_file.write(toWrite)
    traindata_processed_file.close()
    print("Done writing results to file")

    # wb = xw.Book('part2_results.xlsx')
    # sht = wb.sheets['Sheet1']
    # sht.range('A' + str(1 + offset)).value = "Name: "
    # sht.range('B' + str(1 + offset)).value = tree_str
    
    # for i in range(offset + 4, offset + 4 + len(attacktypes_set)):
    #     num = 'A' + str(i)
    #     sht.range(num).value = attacktypes_set[i - 4 - offset]

    # alphas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    # for i in range(1, 1 + len(attacktypes_set)):
    #     num = alphas[i] + str(3 + offset)
    #     sht.range(num).value = attacktypes_set[i - 1]

    # for i in range(offset + 4, offset + 4 + len(attacktypes_set)):
    #     for j in range(1, 1 + len(attacktypes_set)):
    #         num = alphas[j] + str(i)
    #         sht.range(num).value = confusion_matrix[attacktypes_set[i-4-offset]][attacktypes_set[j-1]]

    # sht.range('A' + str(10 + offset)).value = "Accuracy:"
    # sht.range('B' + str(10 + offset)).value = score

    offset += 13

    return offset



def doTest(classifier):

    graph = classifier[0]
    #all_combs_probs = classifier[1]
    if DEBUG:
        for k in all_combs_probs.keys():
            print k

    pars_g = transpose(graph)

    confusion_matrix = {}
    for i in ['Y','N']:
        confusion_matrix[i] = {}
        for j in ['Y','N']:
            confusion_matrix[i][j] = 0

    for j in range(len(testdata)):

        prob_class = {}
        for e in ['Y','N']:
            prob = 1.0
            attrs = testdata[j]
            #for j in range(len(attrs)):


            for i in range(5):

                child = i
                c_val = None
                if child < 3:
                    c_val = attrs[i]
                elif child == 3:
                    c_val = e
                elif child == 4:
                    c_val = attrs[3]

                pars = segregate(pars_g[child], 1)
                val_list = []
                val_list.append((child, c_val))
                for p in pars:
                    p_val = None

                    if p < 3:
                        p_val = attrs[p]
                    elif p == 3:
                        p_val = e
                    elif p == 4:
                        p_val = attrs[3]

                    val_list.append((p, p_val))

                val_tuple = tuple(val_list)
                prob = prob * math.log(all_combs_probs[val_tuple])

            # if DEBUG:
            #     if(int(all_combs_probs[val_tuple] * 1000000) == 0):
            #         print(val_tuple, all_combs_probs[val_tuple])
            #sum_log_probs = sum_log_probs + math.log(all_combs_probs[val_tuple])
            # if(i > 1117000):
            #   print("~~~~~~~~~~~~~")
            #   print ("e", e)
            #   print ("j", j)
            #   print ("attrs", attrs)
            #   print("classifier[0][e][j]", classifier[0][str(e)][j])

            # if(str(attrs[j]) in classifier[0][e][j].keys()):
            #   # print("~~~~~~~~~~~~~~~~~~~~~~~~")
            #   # print((classifier[0][e][j][str(attrs[j])] * 1.0))
            #   # print((classifier[1][e][j] * 1.0))
            #   prob = prob * (((classifier[0][e][j][str(attrs[j])] * 1.0) + SMOOTH_E)  / ((classifier[1][e][j] * 1.0) + (SMOOTH_E * len(classifier[0][e][j].keys()))))
            #   #print(prob)
            # else:
            #   prob = prob * ((SMOOTH_E * 1.0) / (classifier[1][e][j] + (SMOOTH_E * len(classifier[0][e][j].keys()))))

        #prob = prob * ((classifier[2][str(e)] * 1.0) / classifier[3])
            prob_class[str(e)] = prob 

        cur_max = -1.0
        max_class = None

        for k in prob_class.keys():
            if(prob_class[k] > cur_max):
                cur_max = prob_class[k]
                max_class = k

        result = max_class
        confusion_matrix[testdata_results[j]][result] = confusion_matrix[testdata_results[j]][result] + 1
        #print(prob_class)
        if(j % 100 == 0):
            print("Done testing " + str(j) + " instances...")

    print(confusion_matrix)
    return (confusion_matrix, classifier[0])


offset = 0

# Part 1 Testing
classifier_str = "processed_stuff/bayes_net"
(c_matrix, graph) = doTest(loadClassifier(classifier_str))
offset = calc_and_save(classifier_str, c_matrix, graph, offset)





