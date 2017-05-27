10-601: Machine Learning
Author: Maher Khan (mhkhan)

Midterm

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

NOTE: If you just want to test the models, then skip steps 1 to 4 and only
      do Step 5 and 6 (the models are already in the correct folders)

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
data:
	python part1_parser.py
	python testdata_parser.py
	python part2_parser.py

Step 3) For part 1 of the homwork, run the following programs in the folder 
"part_1" with python in terminal/command in this order:
	python naive_bayes_classifier.py

Step 4) For part 2 of the homwork, run the following programs in the folder 
"part_2" with python in terminal/command in this order:
	python graphs.py
	python map.py

Step 5) In order to evaluate:, just run the following 
python program in the main directory in the terminal/command:
	python part1_validator.py
	python part2_validator.py (NOTE: this one is in part_2 folder)

Step 6) The results should be automatically generated in "part1_results.xlsx" 
    and "part2_results.xlsx" files in the main directory.


