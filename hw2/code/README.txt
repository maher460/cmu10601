10-601: Machine Learning
Author: Maher Khan (mhkhan)

HOMEWORK 2

Dependencies:
Python 2.7

modules:
xlwings
jsonpickle
json
random
math
sys
heapq

Here are the step by step instructions to run the code for all the parts:

NOTE: If you just want to test the models, then skip steps 1 to 5 and only
      do Step 6 and 7 (the models are already in the correct folders)

Step 1) Place the correct data files with the correct names in the "data" 
subfolder of the main directory:
	data/attacktypes.list
	data/intrusion.features
	data/intrusion.testdata
	data/intrusion.testlabels.categorized
	data/intrusion.traindata
	data/intrusion.validationdata

Step 2) Run the following parser programs in the main directory with python 
in terminal/command in order to parse, quantize and categorize the train, test 
and validation data:
	python parser.py
	python parser_testdata.py
	python parser_validationdata.py

Step 3) For part 1 of the homwork, run the following programs in the folder 
"part_1" with python in terminal/command in this order:
	python train_dtree.py
	python python prune_dtree_i.py
	python python prune_dtree_ii.py

Step 3) For part 2 of the homwork, run the following programs in the folder 
"part_2" with python in terminal/command in this order:
	python train_dtree.py
	python python prune_dtree_i.py
	python python prune_dtree_ii.py

Step 4) For part 3 of the homwork, run the following program in the folder 
"part_3" with python in terminal/command:
	python train_bagged_dtree_forest.py

Step 5) For part 4 of the homwork, run the following program in the folder 
"part_4" with python in terminal/command:
	python train_random_forest.py

Step 6) In order to evaluate all the trees at once, just run the following 
python program in the main directory in the terminal/command:
	python validator.py

 	(NOTE: if you want to evaluate certain trees or certai parts of the 
 	 homework, please comment out the irrelevant function calls in the 
 	 validator.py file)

Step 7) The results should be automatically generated in "Results.xlsx" file
in the main directory.


