import sys
from sys import path
import os
import csv 
import collections
from collections import OrderedDict
from math import fabs
#from ShevaDB import ShevaDB

class ShevaUtils:

    def __init__(self):
        """
        this.baza = ShevaDB()
        print "ShevaUtils created"
        """
        pass
    
    def __del__(self):
        """
        print 'ShevaUtils destroyed'
        """
        pass
        
    def checkIfList(self, data):
        if type(data) is not list and type(data) is not tuple:
            sys.exit("Wrong filetype: needed iterable")
            
    
    def getUniqueItems(self, inlist, indeks):
        """
        Return uniqe values from column indeks from either list or csv file inlist
        """
        uniques = []
        rownum = 0
        
        if type(inlist) is str:
            f = open(inlist, "rb") # don't forget the 'b'!
            inlist = csv.reader(f)
        
        #iterate through csv, return values in row under column indeks
        for item in inlist:
            if item[indeks] not in uniques:
                #print item[indeks]
                uniques.append(item[indeks])
        return uniques
    
    def getCSV_Colmn(self, file,column):
        returnValues = []
        rownum = 0
        mycsv = csv.reader(open(file))
        for row in mycsv:
            if rownum == 0:
                header = row
                #print row
            else:        
                returnValues.append(row[column])
            rownum += 1
        return returnValues
    
    def summaryGraph(self, a,b,labels,name,model):
        for x, y in zip(a, b):
          plt.plot(range(2,15), x)
          plt.plot(range(2,15), y)
    
        plt.legend(labels, ncol=2, loc=1, 
               bbox_to_anchor=[0.5, 1.1], 
               columnspacing=1.0, labelspacing=0.0,
               handletextpad=0.0, handlelength=1.5,
               fancybox=True, shadow=True)
        plt.xlabel("Depth")
        plt.ylabel("Number of documents")
        plt.title("Documents in model vs returned documents")
        #plt.setp(gca().get_legend().get_texts(), fontsize='10')
        name = "testData_classificationModels/%s/%s.png" %(model,name)
        plt.savefig(name)
    
    def returnDirectoryList(self, diskPath):
        directories = []
        for files in os.listdir(diskPath): 
            if os.path.isdir(os.path.join(diskPath,files)):
                directories.append(files)
        return directories
    
    def createDir(self, rootDir,groupType,model):
        try:
            #basic directory for grouping type: type
            diskPath = "%s/%s/" %(rootDir,groupType)
            if not os.path.isdir(diskPath):
                os.mkdir(diskPath)
        
            #basic directory for model, based on % of data being analyzed
            modelPath = "%s/%s/"%(diskPath,model)
            if not os.path.isdir(modelPath):
                os.mkdir(modelPath)
                
            #path to dict, model, corpusFiles directory, sim, labels, origCATID directories
            pathSubDir = ["dict/","models/","corpus/","originalID/","sim/"]
            for pathItem in pathSubDir:
                checkPath = "%s%s" %(modelPath,pathItem)
                if not os.path.isdir(checkPath):
                    os.mkdir(checkPath)
        except ValueError:
            print "Oops!  Directory creation not working. %s,\t,%s,\t,%s" %(rootDir,groupType,model)
    
    def createDirOne(self,dir):
        if not os.path.isdir(dir):
            os.mkdir(dir)
            
    def setLimit(self,percentageItem,data):
        length = (percentageItem*len(data))/100
        if length == 0:
            length = 1
        return length
    
    def euclidean(self, x,y):
        sumSq=0.0
        #print "x:", x
        #print "y:", y
        #add up the squared differences
        for i in range(len(x)):
            #print "x[i]", x[i], type(x[i])
            #print "y[i]", y[i], type(y[i])
            sumSq+=(x[i]-y[i])**2
     
        #take the square root of the result
        return (sumSq**0.5)
    
    def explodeList(self, list, delimiter):
        pass
    
    def analyzeRecommendationDict(self, dict1, dict2):
        
        results = OrderedDict()
        
        for key in dict1.keys():
            cat1 = dict1[key]
            cat2 = dict2[key]
            
            if len(cat1) == len(cat2):
                catLen = 0
                for i in range(len(cat1)):
                    catLen += fabs(cat1[i]-cat2[i])
            else:
                catLen = -1

            results[key] = catLen
    
        return results
    
