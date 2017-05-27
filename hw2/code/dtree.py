#-------- The Dtree code ------------

#Here "attributes" is an Num-instance x Num-attributes matrix. Each row is
#one training instance.
#"labels" is a Num-instance x 1 array of class labels for the training instances

# Note, we're storing a number of seemingly unnecessary variables, but
# we'll use them later for counting and pruning

# This is just to define the attributes of the Dtree class to be used with the validator

class Dtree:

    c_nodeGainRatio = None
    c_nodeInformationGain = None
    c_isLeaf = None
    c_majorityClass = None
    c_bestAttribute = None
    c_children = None
    c_parent = None

