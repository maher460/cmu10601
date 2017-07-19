# import json

# print("Loading centroids...")
# traindata_processed_file = open("parsed_data/data1.kmeanspartialcentroids", "r")
# centroids = json.loads(traindata_processed_file.read())
# traindata_processed_file.close()
# print("Done loading centroids!")

# print ("len(centroids): ", len(centroids))

# print ("len(centroids[0]): ", len(centroids[0]))

# print ("len(centroids[-1]): ", len(centroids[-1]))

b = (-1)
for i in range(3):

	def a(x):
		print (x, b, i)

	a(0)
	b = i
	a(1)
