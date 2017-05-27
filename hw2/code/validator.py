import dtree
import jsonpickle
import json
import xlwings as xw

DEBUG = False


testdata_results_file = open("data/intrusion.testlabels.categorized", "r")
testdata_results_str = testdata_results_file.read()
testdata_results = testdata_results_str.split("\n")
testdata_results = testdata_results[:-1]


print("Reading attacktypes from file...")
attacktypes_file = open("data/attacktypes.list", "r")
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

print("Loading processed test data")
testdata_processed_file = open("processed_data/intrusion.testdataprocessed", "r")
testdata = json.loads(testdata_processed_file.read())
testdata_processed_file.close()
print("TESTDATA loaded...")

def loadTree(tree_str):
	print("About to load dtree")
	traindata_processed_file = open(tree_str, "r")
	trained_dtree = jsonpickle.decode(traindata_processed_file.read())
	traindata_processed_file.close()
	print("trained dtree loaded")
	return trained_dtree

def calc_and_save(tree_str, confusion_matrix, offset):
	correct = 0
	for e in attacktypes_set:
		correct = correct + confusion_matrix[e][e]

	print(((correct * 1.0) / len(testdata)) * 100)

	score = (((correct * 1.0) / len(testdata)) * 100)

	wb = xw.Book('Results.xlsx')
	sht = wb.sheets['Sheet1']
	sht.range('A' + str(1 + offset)).value = "Name: "
	sht.range('B' + str(1 + offset)).value = tree_str
	
	for i in range(offset + 4, offset + 4 + len(attacktypes_set)):
		num = 'A' + str(i)
		sht.range(num).value = attacktypes_set[i - 4 - offset]

	alphas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
	for i in range(1, 1 + len(attacktypes_set)):
		num = alphas[i] + str(3 + offset)
		sht.range(num).value = attacktypes_set[i - 1]

	for i in range(offset + 4, offset + 4 + len(attacktypes_set)):
		for j in range(1, 1 + len(attacktypes_set)):
			num = alphas[j] + str(i)
			sht.range(num).value = confusion_matrix[attacktypes_set[i-4-offset]][attacktypes_set[j-1]]

	sht.range('A' + str(10 + offset)).value = "Accuracy:"
	sht.range('B' + str(10 + offset)).value = score

	offset += 13

	return offset



def doTest(tree):

	confusion_matrix = {}
	for i in attacktypes_set:
		confusion_matrix[i] = {}
		for j in attacktypes_set:
			confusion_matrix[i][j] = 0

	for i in range(len(testdata)):
		temp = tree
		result = None
		while(temp != None):
			#print(temp["c_isLeaf"])
			#print(temp.c_majorityClass)
			result = temp.c_majorityClass
			
			if DEBUG:
				print("---------------------")
				print(testdata[i])
				print(temp.c_bestAttribute)

			if(temp.c_children != None):

				if DEBUG:
					print(temp.c_children.keys())

				if(temp.c_bestAttribute != None):
					key = str(testdata[i][temp.c_bestAttribute])

					if DEBUG:
						print("key: " + key)

					if(key in temp.c_children.keys()):
						temp = temp.c_children[key]
					else:
						temp = None
				else:

					if DEBUG: 
						print("temp.c_bestAttribute is None")
					temp = None
			else:

				if DEBUG:
					print("No children")
				temp = None
			
			if DEBUG:
				print("---------------------")
		
		if DEBUG:
			print("~~~~~~~~~~~~~~~~~~~~~~~")
			print("~~~~~~~~~~~~~~~~~~~~~~~")
			print("Result: " + str(result))
			print("~~~~~~~~~~~~~~~~~~~~~~~")
			print("~~~~~~~~~~~~~~~~~~~~~~~")

		confusion_matrix[testdata_results[i]][result] = confusion_matrix[testdata_results[i]][result] + 1

		if(i % 10000 == 0):
			print("Done testing " + str(i) + " instances...")

	print(confusion_matrix)
	return confusion_matrix

def doTest2(trees):

	confusion_matrix = {}
	for i in attacktypes_set:
		confusion_matrix[i] = {}
		for j in attacktypes_set:
			confusion_matrix[i][j] = 0

	for i in range(len(testdata)):
		count = {}
		for j in attacktypes_set:
			count[j] = 0

		for tree in trees:
			temp = tree
			result = None
			while(temp != None):
				#print(temp["c_isLeaf"])
				#print(temp.c_majorityClass)
				result = temp.c_majorityClass
				
				if DEBUG:
					print("---------------------")
					print(testdata[i])
					print(temp.c_bestAttribute)

				if(temp.c_children != None):

					if DEBUG:
						print(temp.c_children.keys())

					if(temp.c_bestAttribute != None):
						key = str(testdata[i][temp.c_bestAttribute])

						if DEBUG:
							print("key: " + key)

						if(key in temp.c_children.keys()):
							temp = temp.c_children[key]
						else:
							temp = None
					else:

						if DEBUG: 
							print("temp.c_bestAttribute is None")
						temp = None
				else:

					if DEBUG:
						print("No children")
					temp = None
				
				if DEBUG:
					print("---------------------")
			
			if DEBUG:
				print("~~~~~~~~~~~~~~~~~~~~~~~")
				print("~~~~~~~~~~~~~~~~~~~~~~~")
				print("Result: " + str(result))
				print("~~~~~~~~~~~~~~~~~~~~~~~")
				print("~~~~~~~~~~~~~~~~~~~~~~~")

			count[result] = count[result] + 1

		cur_max = -1
		max_res = None
		for k in count.keys():
			if(count[k] > cur_max):
				cur_max = count[k]
				max_res = k

		result = max_res

		confusion_matrix[testdata_results[i]][result] = confusion_matrix[testdata_results[i]][result] + 1

		if(i % 10000 == 0):
			print("Done testing " + str(i) + " instances...")

	print(confusion_matrix)
	return confusion_matrix


offset = 0

# Part 1 Testing
tree_str = "part_1/processed_trees/intrusion.traineddtree"
c_matrix = doTest(loadTree(tree_str))
offset = calc_and_save(tree_str, c_matrix, offset)

tree_str = "part_1/processed_trees/intrusion.pruned1dtree30"
c_matrix = doTest(loadTree(tree_str))
offset = calc_and_save(tree_str, c_matrix, offset)

tree_str = "part_1/processed_trees/intrusion.pruned1dtree20"
c_matrix = doTest(loadTree(tree_str))
offset = calc_and_save(tree_str, c_matrix, offset)

tree_str = "part_1/processed_trees/intrusion.pruned1dtree10"
c_matrix = doTest(loadTree(tree_str))
offset = calc_and_save(tree_str, c_matrix, offset)

tree_str = "part_1/processed_trees/intrusion.pruned2dtree30"
c_matrix = doTest(loadTree(tree_str))
offset = calc_and_save(tree_str, c_matrix, offset)

tree_str = "part_1/processed_trees/intrusion.pruned2dtree20"
c_matrix = doTest(loadTree(tree_str))
offset = calc_and_save(tree_str, c_matrix, offset)

tree_str = "part_1/processed_trees/intrusion.pruned2dtree10"
c_matrix = doTest(loadTree(tree_str))
offset = calc_and_save(tree_str, c_matrix, offset)

# Part 2 Testing
tree_str = "part_2/processed_trees/intrusion.traineddtree"
c_matrix = doTest(loadTree(tree_str))
offset = calc_and_save(tree_str, c_matrix, offset)

tree_str = "part_2/processed_trees/intrusion.pruned1dtree30"
c_matrix = doTest(loadTree(tree_str))
offset = calc_and_save(tree_str, c_matrix, offset)

tree_str = "part_2/processed_trees/intrusion.pruned1dtree20"
c_matrix = doTest(loadTree(tree_str))
offset = calc_and_save(tree_str, c_matrix, offset)

tree_str = "part_2/processed_trees/intrusion.pruned1dtree10"
c_matrix = doTest(loadTree(tree_str))
offset = calc_and_save(tree_str, c_matrix, offset)

tree_str = "part_2/processed_trees/intrusion.pruned2dtree30"
c_matrix = doTest(loadTree(tree_str))
offset = calc_and_save(tree_str, c_matrix, offset)

tree_str = "part_2/processed_trees/intrusion.pruned2dtree20"
c_matrix = doTest(loadTree(tree_str))
offset = calc_and_save(tree_str, c_matrix, offset)

tree_str = "part_2/processed_trees/intrusion.pruned2dtree10"
c_matrix = doTest(loadTree(tree_str))
offset = calc_and_save(tree_str, c_matrix, offset)

# Part 3 Testing
trees_str = "part_3/processed_trees/intrusion.baggeddtreeforest"
c_matrix = doTest2(loadTree(trees_str))
offset = calc_and_save(trees_str, c_matrix, offset)

# Part 4 Testing
trees_str = "part_4/processed_trees/intrusion.randomforest"
c_matrix = doTest2(loadTree(trees_str))
offset = calc_and_save(trees_str, c_matrix, offset)




