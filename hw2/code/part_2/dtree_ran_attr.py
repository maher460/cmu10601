import math
import sys 
import random

DEBUG = False

#------- Some "Helper" functions ---------------
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

# Assuming labels take values 1..M.
def computeEntropy(labels):
    entropy = 0.0
    for v in unique_labels(labels):
        probability_i = (len(segregate(labels, v)) * 1.0) / len(labels)
        entropy -= probability_i * math.log(probability_i, 2)
    return entropy

def computeEntropyAttrCount(attributeCount):
    entropy = 0.0
    total = 0
    for v in attributeCount.values():
        total = total + v
    for k in attributeCount.keys():
        probability_i = (attributeCount[k] * 1.0) / total
        entropy -= probability_i * math.log(probability_i, 2)
    return entropy


# Find most frequent value. Assuming labels take values 1..M 
def mostFrequentlyOccurringValue(labels):
    bestCount = float('-inf')
    bestId = None
    for v in unique_labels(labels):
        count_i = len(segregate(labels, v))
        if (count_i > bestCount):
            bestCount = count_i
            bestId = v
    return bestId

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

def select_labels(labels, ids):
    result = []
    for i in ids:
        result.append(labels[i])
    return result



#-------- The Dtree code ------------

#Here "attributes" is an Num-instance x Num-attributes matrix. Each row is
#one training instance.
#"labels" is a Num-instance x 1 array of class labels for the training instances

# Note, we're storing a number of seemingly unnecessary variables, but
# we'll use them later for counting and pruning

class Dtree:

    c_nodeGainRatio = None
    c_nodeInformationGain = None
    c_isLeaf = None
    c_majorityClass = None
    c_bestAttribute = None
    c_children = None
    c_parent = None


    def buildTree(self, attributes, labels):

        print("Number of instances for this run of buildTree: " + str(len(labels)))
        
        if DEBUG:
            print("starting build tree...")
        numInstances = len(labels)
        nodeInformation = numInstances * computeEntropy(labels)
        self.c_majorityClass = mostFrequentlyOccurringValue(labels)

        if DEBUG:
            print("done nodeInfo and c_majority_class....")
            print("majorityClass: " + str(self.c_majorityClass))
            print("nodeInfo: " + str(nodeInformation))


        if(int(nodeInformation) == 0):
            self.c_isLeaf = True
            return
        else:
            self.c_isLeaf = False

        bestAttribute = None
        bestInformationGain = float('-inf')
        bestGainRatio = float('-inf')

        attributes_t = transpose(attributes)

        if DEBUG:
            print("done transposing matrix....")

        for i in random.sample(range(len(attributes_t)), 1):

            attributeCount = {}
            conditionalInfo = 0.0
            attributeEntropy = 0.0

            for v in unique_labels(attributes_t[i]):

                if DEBUG:
                    print("starting work on attribute and value " + str(i) + ", " + str(v))

                ids = segregate(attributes_t[i], v)

                if DEBUG:
                    print("done segregating ids...")
                    print("len ids: " + str(len(ids)))
                
                attributeCount[v] = len(ids)
                label_ids = select_labels(labels, ids)
                conditionalInfo += attributeCount[v] * computeEntropy(label_ids);

            if DEBUG:
                print("done with values...")
            attributeInformationGain = nodeInformation - conditionalInfo

            if DEBUG:
                print("attributeInformationGain: " + str(attributeInformationGain))
            compEntAttrCnt = computeEntropyAttrCount(attributeCount)
            if compEntAttrCnt != 0:
                gainRatio = (attributeInformationGain * 1.0) / compEntAttrCnt

                if DEBUG:
                    print("gainRatio: " + str(gainRatio))

                if (gainRatio > bestGainRatio):
                    bestInformationGain = attributeInformationGain
                    bestGainRatio = gainRatio
                    bestAttribute = i

        if DEBUG:
            print("done with main part....")

        #If no attribute provides any gain, this node cannot be split further
        if (bestGainRatio <= -sys.maxint - 1):
            bestGainRatio = -sys.maxint - 1
        if (bestGainRatio >= sys.maxint):
            bestGainRatio = sys.maxint
        if (int(bestGainRatio) == 0) or (bestAttribute == None):
            self.c_isLeaf = True
            return


        # Otherwise split by the best attribute
        self.c_bestAttribute = bestAttribute
        self.c_nodeGainRatio = bestGainRatio
        self.c_nodeInformationGain = bestInformationGain
        self.c_children = {}

        if DEBUG:
            print("\n(inner)building tree...")
            print("isLeaf: " + str(self.c_isLeaf))
            print("bestAttr: " + str(self.c_bestAttribute))
            print("majorityClass: " + str(self.c_majorityClass))


        for v in unique_labels(attributes_t[bestAttribute]):
            ids = segregate(attributes_t[bestAttribute], v)
            new_attributes = []
            new_labels = []
            for i in ids:
                new_attributes.append(attributes[i])
                new_labels.append(labels[i])
            self.c_children[v] = Dtree(new_attributes, new_labels)
            self.c_children[v].c_parent = self
        return




    def __init__(self, attributes, labels):
        self.c_parent = None
        self.buildTree(attributes, labels)

        if DEBUG:
            print("\nbuilding tree...")
            print("isLeaf: " + str(self.c_isLeaf))
            print("bestAttr: " + str(self.c_bestAttribute))
            print("majorityClass: " + str(self.c_majorityClass))
            print("parent: " + str(self.c_parent))
            if self.c_children:
                print("children: " + str(self.c_children.keys()))
