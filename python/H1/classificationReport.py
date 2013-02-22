import os, csv, operator
from docutils.utils import uniq
from collections import Counter, defaultdict, OrderedDict

#functionality
#get list of subdirectories of path
def returnDirectoryList(path):    
    directories = []
    
    for files in os.listdir(path): 
        if os.path.isdir(os.path.join(path,files)):
            #print "Directory : ",files
            directories.append(files)
    return directories

#get unique fileds in csv, ignore header line
def uniq(inlist, indeks):     
    #variables
    uniques = []
    rownum = 0
    
    #iterate through csv, return values in row under column indeks
    for item in inlist:
        if rownum == 0:
            header = item
            #print row
        else:
            if item[indeks] not in uniques:
                #print item[indeks]
                uniques.append(item[indeks])
        rownum += 1
    return uniques

#open csv for reading

def analyzeCSV(modelPath,fileName):
    pathOID = "testData/"+modelPath+"/origCATID/"+fileName
    pathSIM = "testData/"+modelPath+"/sim/"+fileName
    originalRowID = []
    # a dictionary whose value defaults to a list.
    
    data = defaultdict(list)
    dataSorted =defaultdict(list) 
    # open the csv file and iterate over its rows. the enumerate()
    # function gives us an incrementing row number
    for i, row in enumerate(csv.reader(open(pathSIM, 'rb'))):
        # skip the header line and any empty rows
        # we take advantage of the first row being indexed at 0
        # i=0 which evaluates as false, as does an empty row
        if not i or not row:
            continue
        # unpack the columns into local variables
        print row
        category,level,catID,matrixRow, similarity= row
        print category,"    ", level,"    ",catID,matrixRow,"    ",similarity
        # for each zipcode, add the level the list
        data[matrixRow].append(float(similarity))
        
    #print data
    # loop over each zipcode and its list of levels and calculate the average
    
    for zipcode, levels in data.iteritems():
        #print zipcode, levels, sum(levels)
        pass

    for row in data.iteritems():
        print row[0], sum(row[1]), len(row[1])
        dataSorted[row[0]].append(sum(row[1]))
    
    #print dataSorted
    #print len(dataSorted)
        
    #print dataSorted
    sorted_x = sorted(dataSorted.iteritems(), key=lambda x: (x[1],x[0]), reverse=True)
    sorted_xx = sorted(dataSorted.iteritems(), key=lambda x: (x[0],x[1]), reverse=True)

    print sorted_x
    print len(sorted_x)
    print sorted_xx
    print len(sorted_xx)    

    #open original csv with original categories
    matrixID = [x[0] for x in sorted_x]
    #print matrixID
        
    for row in csv.reader(open(pathOID, 'rb')):
        #print row
        if row[0] in matrixID:
            #print row[0], row[1]
            originalRowID.append(row[1])

    originalRowID = [row[1] for row in csv.reader(open(pathOID, 'rb')) if row[0] in matrixID]
    print originalRowID

#print returnDirectoryList('testData')
analyzeCSV('0.1','0.1_Arts_3.csv')
