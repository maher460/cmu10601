import json

DEBUG = False

def filename_parser(list_file):

    print ("     Reading list_file: '" + list_file + "' ...")
    traindata_file = open(list_file, "r")
    traindata_str = traindata_file.read()
    traindata = traindata_str.split("\n")

    traindata = traindata[:-1]

    traindata_file.close()
    return traindata

def parse(filename, result=[]):

    print ("     Reading data from filename: '" + filename + "' ...")
    traindata_file = open(filename, "r")
    traindata_str = traindata_file.read()
    traindata = traindata_str.split("\n")

    for idx, item in enumerate(traindata):
        item = item.split("  ")
        #item[-1] = item[-1][:-1]
        # if DEBUG:
        #     print item[1:]
        #     print map(float,item[1:])
        traindata[idx] = map(float,item[1:])
        # if(idx % 100 == 0):
        #     print("Done reading " + str(idx) + " data")
    traindata = traindata[:-1]

    if DEBUG:
        #print traindata
        print ("len(traindata): ", len(traindata))
        print ("len(traindata[0]): ", len(traindata[0]))
        print ("len(traindata[-1]): ", len(traindata[-1]))

    result.extend(traindata)

    traindata_file.close()
    return result


def all_parser(list_file_name, result=[]):

    files_list = filename_parser(list_file_name)

    if DEBUG:
        print ("files_list: ", files_list)

    for filename in files_list:
        proper_path = "../endsemdata/" + filename
        parse(proper_path, result)

    if DEBUG:
        #print result
        print ("len(result): ", len(result))
        print ("len(result[0]): ", len(result[0]))
        print ("len(result[-1]): ", len(result[-1]))

def save_result(result, filename):
    print("     Writing parsed data to file...")
    traindata_processed_file = open(("parsed_data/" + filename), "w")
    traindata_processed_file.write(json.dumps(result))
    traindata_processed_file.close()
    print("     Done writing parsed data to file")




#################
# MAIN

list_files = [
                "../endsemdata/lists/101.traininglist",
                # "../endsemdata/lists/102.traininglist",
                # "../endsemdata/lists/103.traininglist",
                # "../endsemdata/lists/104.traininglist",
                # "../endsemdata/lists/105.traininglist",
                # "../endsemdata/lists/106.traininglist",
                # "../endsemdata/lists/107.traininglist",
                # "../endsemdata/lists/108.traininglist",
                # "../endsemdata/lists/109.traininglist",
                # "../endsemdata/lists/110.traininglist",
             ]

print ("---> Starting to parse data...")
result = []
for list_file_name in list_files:
    print ("---> About to parse from the list_file: '" + list_file_name + "' ...")
    all_parser(list_file_name, result)

print "---> Done parsing all data!"
print ("Total: ", len(result))

if DEBUG:
    #print result
    print ("len(result): ", len(result))
    print ("len(result[0]): ", len(result[0]))
    print ("len(result[-1]): ", len(result[-1]))

save_result(result, "data1_small.universalenrollparsed")

print ("---> Everything has completed successfully!")


