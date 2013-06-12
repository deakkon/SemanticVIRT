import sys
from sys import path
import os
import csv 
import collections
from ShevaDB import ShevaDB

class ShevaUtils:

    def __init__(self):
        """
        this.baza = ShevaDB()
        """
        pass
        
    def checkIfList(self, data):
        if type(data) is not list and type(data) is not tuple:
            sys.exit("Wrong filetype: needed iterable")
    
    def getUniqueItems(self, inlist, indeks=""):
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
    
    def returnDirectoryList(self, path):
        directories = []
        for files in os.listdir(path): 
            if os.path.isdir(os.path.join(path,files)):
                directories.append(files)
        return directories
    
    def createDir(self, rootDir,groupType,model):
        try:
            #basic directory for grouping type: type
            path = "%s/%s/" %(rootDir,groupType)
            if not os.path.isdir(path):
                os.mkdir(path)
        
            #basic directory for model, based on % of data being analyzed
            modelPath = "%s/%s/"%(path,model)
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