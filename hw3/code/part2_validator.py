import jsonpickle
import json
import xlwings as xw

DEBUG = False
SMOOTH_E = 0.1

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
testdata_processed_file = open("processed_data/intrusion.kmeanstestdataprocessed", "r")
testdata = json.loads(testdata_processed_file.read())
testdata_processed_file.close()
print("TESTDATA loaded...")

def loadClassifier(classifier_str):
	print("About to load dtree")
	traindata_processed_file = open(classifier_str, "r")
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

	wb = xw.Book('part2_results.xlsx')
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



def doTest(classifier):

	confusion_matrix = {}
	for i in attacktypes_set:
		confusion_matrix[i] = {}
		for j in attacktypes_set:
			confusion_matrix[i][j] = 0

	for i in range(len(testdata)):

		prob_class = {}
		for e in attacktypes_set:
			prob = 1.0
			attrs = testdata[i]
			for j in range(len(attrs)):
				# if(i > 1117000):
				# 	print("~~~~~~~~~~~~~")
				# 	print ("e", e)
				# 	print ("j", j)
				# 	print ("attrs", attrs)
				# 	print("classifier[0][e][j]", classifier[0][str(e)][j])

				if(str(attrs[j]) in classifier[0][e][j].keys()):
					# print("~~~~~~~~~~~~~~~~~~~~~~~~")
					# print((classifier[0][e][j][str(attrs[j])] * 1.0))
					# print((classifier[1][e][j] * 1.0))
					prob = prob * (((classifier[0][e][j][str(attrs[j])] * 1.0) + SMOOTH_E)  / ((classifier[1][e][j] * 1.0) + (SMOOTH_E * len(classifier[0][e][j].keys()))))
					#print(prob)
				else:
					prob = prob * ((SMOOTH_E * 1.0) / (classifier[1][e][j] + (SMOOTH_E * len(classifier[0][e][j].keys()))))

			prob = prob * ((classifier[2][str(e)] * 1.0) / classifier[3])
			prob_class[str(e)] = prob 

		cur_max = -1.0
		max_class = None

		for k in prob_class.keys():
			if(prob_class[k] > cur_max):
				cur_max = prob_class[k]
				max_class = k

		result = max_class
		confusion_matrix[testdata_results[i]][result] = confusion_matrix[testdata_results[i]][result] + 1
		#print(prob_class)
		if(i % 1000 == 0):
			print("Done testing " + str(i) + " instances...")

	print(confusion_matrix)
	return confusion_matrix


offset = 0

# Part 1 Testing
classifier_str = "part_2/processed_classifier/intrusion.trainedclassifier"
c_matrix = doTest(loadClassifier(classifier_str))
offset = calc_and_save(classifier_str, c_matrix, offset)





