import dtree_ran_attr
import jsonpickle
import json
from heapq import heappush, heappop

DEBUG = False

# First pass : evaluate validation data and note the classification at each node
# Assuming that "valData" includes "attributes" and "labels"

# First create an empty list of error counts at nodes
def createNodeList(dTree, nodeError):
    nodeError[dTree] = 0
    if(dTree.c_children != None):
        for key in dTree.c_children.keys():
            nodeError = createNodeList(dTree.c_children[key], nodeError)
    return nodeError


# Pass a single instance down the tree and note node errors
def classifyValidationDataInstance(dTree, validationDataInstance, nodeError):
    if (dTree.c_majorityClass != validationDataInstance[-1]):
        nodeError[dTree] += 1
    if (not dTree.c_isLeaf) and (dTree.c_children != None):
        if (dTree.c_bestAttribute != None) and (validationDataInstance[dTree.c_bestAttribute] in dTree.c_children.keys()): 
            childNode = dTree.c_children[validationDataInstance[dTree.c_bestAttribute]]
            nodeError = classifyValidationDataInstance(childNode, validationDataInstance, nodeError)
    return nodeError 


# Count total node errors for validation data
def classifyValidationData(dTree, validationData):
    nodeErrorCounts = createNodeList(dTree, {})
    count = 0
    for instance in validationData:
        nodeErrorCounts = classifyValidationDataInstance(dTree, instance, nodeErrorCounts)

        if count % 10000 == 0:
            print("Done classifying " + str(count) + " validation data")
        count += 1
    return nodeErrorCounts


# Check if a node is a twig
def isTwig(decisionTree):
    if (decisionTree.c_isLeaf) or (decisionTree.c_children == None):
        return False
    for key in decisionTree.c_children.keys():
        if not decisionTree.c_children[key].c_isLeaf:
            return False
    return True


# Count leaves in a tree
def countLeaves(decisionTree):
    if decisionTree.c_isLeaf or (decisionTree.c_children == None):
        return 1
    else:
        n = 0
        for key in decisionTree.c_children.keys():
            child = decisionTree.c_children[key]
            n += countLeaves(child)
        return n



# Second pass:  Create a heap with twigs using nodeErrorCounts
def collectTwigsByErrorCount(dTree, nodeErrorCounts, heap):
    if isTwig(dTree):
        # Count how much the error would increase if the twig were trimmed
        twigErrorIncrease = nodeErrorCounts[dTree]
        for key in dTree.c_children.keys():
            twigErrorIncrease -= nodeErrorCounts[dTree.c_children[key]]
        heappush(heap, (twigErrorIncrease, dTree))
    else:
        if (not dTree.c_isLeaf) and (dTree.c_children != None):
            for key in dTree.c_children.keys():
                heap = collectTwigsByErrorCount(dTree.c_children[key], nodeErrorCounts, heap)
    return heap


# Third pass: Prune a tree to have nLeaves leaves
# Assuming heappop pops smallest value
def pruneByClassificationError(dTree, validationData, nLeaves):
    # First obtain error counts for validation data
    nodeErrorCounts = classifyValidationData(dTree, validationData)
    # Get Twig Heap
    twigHeap = collectTwigsByErrorCount(dTree, nodeErrorCounts, [])

    totalLeaves = countLeaves(dTree)

    while totalLeaves > nLeaves:

        twig = heappop(twigHeap)

        if DEBUG:
            print (twig[0])

        twig = twig[1]
        totalLeaves -= (len(twig.c_children.keys()) - 1) #Trimming the twig removes
                                                    #numChildren leaves, but adds
                                                    #the twig itself as a leaf
        if DEBUG:
            print("--------------------------")
            print(countLeaves(dTree))
            print(len(twig.c_children.keys()))

        for key in twig.c_children.keys():
            twig.c_children[key].c_parent = None

        twig.c_children = None  # Kill the chilren
        twig.c_isLeaf = True
        twig.c_nodeInformationGain = 0

        # Check if the parent is a twig and, if so, put it in the heap
        if twig.c_parent != None:
            parent = twig.c_parent
            if isTwig(parent):
                twigErrorIncrease = nodeErrorCounts[parent]
                if (not parent.c_isLeaf) and (parent.c_children != None):
                    for key in parent.c_children.keys():
                        twigErrorIncrease -= nodeErrorCounts[parent.c_children[key]]
                heappush(twigHeap, (twigErrorIncrease, parent))
        if DEBUG:
            print(countLeaves(dTree))
            print("--------------------------")

    return



# MAIN


print("About to read procesed validation data from file")
validationdata_processed_file = open("../processed_data/intrusion.validationdataprocessed", "r")
validationdata = json.loads(validationdata_processed_file.read())
validationdata_processed_file.close()
print("Processed validation data loaded!")




print("About to load trained dtree")
traindata_processed_file = open("processed_trees/intrusion.traineddtree", "r")
trained_dtree = jsonpickle.decode(traindata_processed_file.read())
traindata_processed_file.close()
print("Trained dtree loaded!")

# Pruning till max 30 leaves
print("Pruning till max 30 leaves")
print("number of leaves before pruning: ", countLeaves(trained_dtree))
pruneByClassificationError(trained_dtree, validationdata, 30)
print("number of leaves after pruning: ", countLeaves(trained_dtree))

print("Writing pruned dtree to file...")
pruned_tree_file = open("processed_trees/intrusion.pruned2dtree30", "w")
pruned_tree_file.write(jsonpickle.encode(trained_dtree))
pruned_tree_file.close()
print("Done writing pruned dtree to file")



print("About to load trained dtree")
traindata_processed_file = open("processed_trees/intrusion.traineddtree", "r")
trained_dtree = jsonpickle.decode(traindata_processed_file.read())
traindata_processed_file.close()
print("Trained dtree loaded!")

# Pruning till max 20 leaves
print("Pruning till max 20 leaves")
print("number of leaves before pruning: ", countLeaves(trained_dtree))
pruneByClassificationError(trained_dtree, validationdata, 20)
print("number of leaves after pruning: ", countLeaves(trained_dtree))

print("Writing pruned dtree to file...")
pruned_tree_file = open("processed_trees/intrusion.pruned2dtree20", "w")
pruned_tree_file.write(jsonpickle.encode(trained_dtree))
pruned_tree_file.close()
print("Done writing pruned dtree to file")



print("About to load trained dtree")
traindata_processed_file = open("processed_trees/intrusion.traineddtree", "r")
trained_dtree = jsonpickle.decode(traindata_processed_file.read())
traindata_processed_file.close()
print("Trained dtree loaded!")

# Pruning till max 10 leaves
print("Pruning till max 10 leaves")
print("number of leaves before pruning: ", countLeaves(trained_dtree))
pruneByClassificationError(trained_dtree, validationdata, 10)
print("number of leaves after pruning: ", countLeaves(trained_dtree))

print("Writing pruned dtree to file...")
pruned_tree_file = open("processed_trees/intrusion.pruned2dtree10", "w")
pruned_tree_file.write(jsonpickle.encode(trained_dtree))
pruned_tree_file.close()
print("Done writing pruned dtree to file")
