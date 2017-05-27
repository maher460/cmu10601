import dtree_ran_attr
import jsonpickle
import json
from heapq import heappush, heappop

DEBUG = False


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


# Check if a node is a twig
def isTwig(decisionTree):
    if (decisionTree.c_isLeaf) or (decisionTree.c_children == None):
        return False
    for key in decisionTree.c_children.keys():
        if not decisionTree.c_children[key].c_isLeaf:
            return False
    return True


# Make a heap of twigs.  The default heap is empty
def collectTwigs(decisionTree, heap):
    if isTwig(decisionTree):
        heappush(heap, (decisionTree.c_nodeInformationGain, decisionTree))
    else:
        if decisionTree.c_children != None:
            for key in decisionTree.c_children.keys():
                child = decisionTree.c_children[key]
                heap = collectTwigs(child, heap)
    return heap


# Prune a tree to have nLeaves leaves
# Assuming heappop pops smallest value
def prune(dTree, nLeaves):
    totalLeaves = countLeaves(dTree)
    twigHeap = collectTwigs(dTree, [])
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
                heappush(twigHeap, (parent.c_nodeInformationGain, parent))
        if DEBUG:
            print(countLeaves(dTree))
            print("--------------------------")

    return


# MAIN



print("About to load trained dtree")
traindata_processed_file = open("processed_trees/intrusion.traineddtree", "r")
trained_dtree = jsonpickle.decode(traindata_processed_file.read())
traindata_processed_file.close()
print("trained dtree loaded")

# Pruning till max 30 leaves
print("Pruning till max 30 leaves")
print("number of leaves before pruning: ", countLeaves(trained_dtree))
prune(trained_dtree, 30)
print("number of leaves after pruning: ", countLeaves(trained_dtree))

print("Writing pruned dtree to file...")
pruned_tree_file = open("processed_trees/intrusion.pruned1dtree30", "w")
pruned_tree_file.write(jsonpickle.encode(trained_dtree))
pruned_tree_file.close()
print("Done writing pruned dtree to file")



print("About to load trained dtree")
traindata_processed_file = open("processed_trees/intrusion.traineddtree", "r")
trained_dtree = jsonpickle.decode(traindata_processed_file.read())
traindata_processed_file.close()
print("trained dtree loaded")

# Pruning till max 20 leaves
print("Pruning till max 20 leaves")
print("number of leaves before pruning: ", countLeaves(trained_dtree))
prune(trained_dtree, 20)
print("number of leaves after pruning: ", countLeaves(trained_dtree))

print("Writing pruned dtree to file...")
pruned_tree_file = open("processed_trees/intrusion.pruned1dtree20", "w")
pruned_tree_file.write(jsonpickle.encode(trained_dtree))
pruned_tree_file.close()
print("Done writing pruned dtree to file")



print("About to load trained dtree")
traindata_processed_file = open("processed_trees/intrusion.traineddtree", "r")
trained_dtree = jsonpickle.decode(traindata_processed_file.read())
traindata_processed_file.close()
print("trained dtree loaded")

# Pruning till max 10 leaves
print("Pruning till max 10 leaves")
print("number of leaves before pruning: ", countLeaves(trained_dtree))
prune(trained_dtree, 10)
print("number of leaves after pruning: ", countLeaves(trained_dtree))

print("Writing pruned dtree to file...")
pruned_tree_file = open("processed_trees/intrusion.pruned1dtree10", "w")
pruned_tree_file.write(jsonpickle.encode(trained_dtree))
pruned_tree_file.close()
print("Done writing pruned dtree to file")