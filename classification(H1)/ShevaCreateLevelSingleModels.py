'''
Created on 9.1.2013.

@author: Jurica Seva

PhD Candidate 
Faculty of Organization and Informatics
University of Zagreb

Functions:
    1. dbQuery(sql)
    2. errorMessage(msg)
    3. removePunct(text)
    4. removeStopWords(text, mode=1)
    5. createCorpusAndVectorModel(data, dataSet, fileName ="", outputFormat=1, modelFormat=1)
    6. getCategoryLabel(categoryLabels,fileName, dataSet)
    7. getCategoryListLevel(catID, fileName, dataset)
    8. getMainCat()
    9. createData(category)
    10. runParallel()
'''
#imports
import sys

#USER DEFINED MODULES
sys.path.append("/home/jseva/SemanticVIRT/_utils/")
from ShevaDB import ShevaDB
from ShevaTPF import ShevaTPF
from ShevaUtils import ShevaUtils
from ShevaVect import ShevaVect
from ShevaCSV import ShevaCSV
#PYTHON MODULES
#import math
import time
import itertools
#import csv
import os
#import string
import pp
#import re
#import itertools
import gc

class createDataSingleLevel:
    
    def __init__(self,type,rootDir):
        """
        type: 1 -> full data
              2 -> limited data
        """

        #percentage of data to be used for model build
        if type == 1:
            self.GROUPTYPE = ["CATID","FATHERID","GENERAL"]
            self.percentageList = [25, 50, 75, 100]
        elif type == 2:
            self.GROUPTYPE = ["GENERAL"]
            self.percentageList = [5]
        else:
            sys.exit("Wrong 'type' parameter in createData.__init__")
        
        self.shevaDB = ShevaDB()
        self.shevaTPF = ShevaTPF()
        self.shevaUtils = ShevaUtils()
        self.shevaVect = ShevaVect()
        self.shevaCSV = ShevaCSV()
        
        if rootDir != "":
            self.shevaUtils.createDirOne(str(rootDir))
            self.rootDir = str(rootDir)
        else:
            sys.exit("Wrong 'rootDir' parameter in createData.__init__")
    
    def createData(self, category):
        """
        1. get root categories to be used and iterate through main categories
        3. get max depth for individual category
        4. from 1 to max till 1 to 1
            get all catid for iterated category
            get all pages for selected categories
            call createCorpusAndVectorModel fro selected documents
        """
        ranger = self.shevaDB.getCategoryDepth(category)
        
        for group in self.GROUPTYPE:
            sqlQueryResults = []
            #gruping dependent queries
            if group == "FATHERID":
                sqlCategory = "select Description, fatherid, categoryDepth from dmoz_combined where mainCategory = '%s'" %(category)
            else:
                sqlCategory = "select Description, catid, categoryDepth from dmoz_combined where mainCategory = '%s'" %(category)
            
            sqlQueryResults = self.shevaDB.dbQuery(sqlCategory)
            
            if sqlQueryResults == 0:
                sys.exit("SQL code error in level: \t", category,"\t",indeks,"\t",sqlCategoryLevel)            
            
            for percentageItem in self.percentageList:
                #data for % model, range data
                dataCategoryLevelAll = []
                dataCategoryLabelAll = []
                originalCatIDAll = []
                dataCategorySingleAll = [[]]
                
                path = "%s/%s/%s/" %(self.rootDir,group,percentageItem)
                self.shevaUtils.createDir(self.rootDir,group,percentageItem)
                
                #var = ""
                
                for indeks in ranger:
                    #var += "Level:\t%s\n" %(indeks)
                    """
                    #gruping dependent queries
                    if group == "FATHERID":
                        sqlCategoryLevel = "select Description, fatherid from dmoz_combined where mainCategory = '%s' and categoryDepth = '%s'" %(category,indeks)
                    else:
                        sqlCategoryLevel = "select Description, catid from dmoz_combined where mainCategory = '%s' and categoryDepth = '%s'" %(category,indeks)
                    
                    sqlQueryResultsLevel = self.shevaDB.dbQuery(sqlCategoryLevel)
                    """
                    
                    sqlQueryResultsLevel = [x for x in sqlQueryResults if x[2] == indeks]
                    
                    #level list variables
                    finalContent = []
                    dataCategoryLevel = []
                    dataCategoryLabel = []
                    originalCatID = []
                    #originalFatherID = []
                        
                    #get unique values
                    if group == "GENERAL":
                        #finalContent = []
                        percentageLevel = self.shevaUtils.setLimit(percentageItem,sqlQueryResultsLevel)
                        finalContent = [[item for item in row[0].split()] for row in sqlQueryResultsLevel[:percentageLevel]]
                        #var += "Original words:\t%s\n" %(finalContent)
                        originalCatID = [row[1] for row in sqlQueryResultsLevel[:percentageLevel]]
                        #var += "Original IDs:\t%s\n" %(originalCatID)
                        dataCategoryLevel.extend(self.shevaTPF.returnClean(finalContent,1))
                        #var += "Processed words:\t%s\n" %(dataCategoryLevel)
                    else:
                        unique = []
                        for row in sqlQueryResultsLevel:
                            if row[1] not in unique:
                                unique.append(row[1])

                        for uniq in unique:
                            #var += "ID:\t%s\n" %(uniq)
                            tempUnique = []
                            tempUnique = [row[0] for row in sqlQueryResultsLevel if row[1] == uniq]
                            percentageLevel = self.shevaUtils.setLimit(percentageItem,tempUnique)
                            tempUnique = [item.split() for item in tempUnique[:percentageLevel]]
                            mergedContent = [i for i in itertools.chain.from_iterable(tempUnique)]
                            #var += "Original words:\t%s\n" %(mergedContent)
                            finalContent.append(mergedContent)
                            originalCatID.append(uniq)
                        dataCategoryLevel.extend(self.shevaTPF.returnClean(finalContent,1))

                    self.shevaUtils.createDir(self.rootDir, group, percentageItem)

                    ##########            FILE NAMES             #################
                    fileNameAll = "%s_%s_1_%s" %(str(percentageItem),category,str(indeks))
                    fileNameLevel = "%s_%s_%s" %(str(percentageItem),category,str(indeks))
                    fileNameSingleAll = "%s_%s_%s" %(str(percentageItem),category,str(indeks))

                    ##########    PRINT OUT ORIGINAL AND PROCESSED DATA  #################
                    """
                    print originalCatID
                    print finalContent
                    print dataCategoryLevel
                    """
                    
                    ##########   ORIGINAL DESCRIPTION AND VECTORIZATION  #################
                    #self.shevaVect.createCorpusAndVectorModel(dataCategoryLevel,fileNameLevel,path)
                    dataCategoryLevelAll.extend(dataCategoryLevel)
                    #self.shevaVect.createCorpusAndVectorModel(dataCategoryLevelAll, fileNameAll,path)
                    
                    #single model for all documents
                    dataCategorySingleAll[0].extend([x for sublist in dataCategoryLevelAll for x in sublist])
                    self.shevaVect.createCorpusAndVectorModel(dataCategorySingleAll, fileNameSingleAll, path)
                    
                    ##########   ORIGINAL CATEGORIES ID   #################
                    #self.shevaUtils.getCategoryListLevel(originalCatID,fileNameLevel,path)
                    originalCatIDAll.extend(originalCatID)
                    #self.shevaCSV.getCategoryListLevel(originalCatIDAll,fileNameAll,path)
                    
                    #print out number of documents for (cat,level,model)
                    print "Done with:\t",group,"\t",category,"\t",indeks,"\t",percentageItem

                    #######################    GC    #################
                    del dataCategoryLevel
                    del originalCatID
                    gc.collect()
                    
                del dataCategoryLevelAll
                del dataCategoryLabelAll
                del originalCatIDAll
                del dataCategorySingleAll
            del sqlQueryResults
            gc.collect()

#PARALEL PYTHON
#def runParallel():
"""
Run comparison on n processors
"""

# tuple of all parallel python servers to connect with
ppservers = ()
#ppservers = ("10.0.0.1",)

if len(sys.argv) > 1:
    ncpus = int(sys.argv[1])
    # Creates jobserver with ncpus workers
    job_server = pp.Server(ncpus, ppservers=ppservers)
else:
    # Creates jobserver with automatically detected number of workers
    job_server = pp.Server(ppservers=ppservers)

print "Starting pp with", job_server.get_ncpus(), "workers"
start_time = time.time()

#initialize and start
rootDirectory = raw_input("Input root directory to store files (keyboard input): ")
#print "%s\n%s\n%s\n" %(dataModel.GROUPTYPE,dataModel.percentageList,dataModel.rootDir)

#start PP[]
jobs = []
inputs = ShevaDB().getMainCat()
#inputs =["Regional"]
for index in inputs:
    print index
    dataModel = createDataSingleLevel(1,rootDirectory)
    print dataModel.GROUPTYPE
    print dataModel.percentageList
    print dataModel.rootDir
    jobs.append(job_server.submit(dataModel.createData, 
                                  (index,),
                                  depfuncs = (),
                                  modules = ("time","ShevaLevelModels","ShevaDB","ShevaTPF","ShevaUtils","ShevaVect","gc","itertools",)))

for job in jobs:
    result = job()
    if result:
        break
#prints
job_server.print_stats()
print "Time elapsed: ", time.time() - start_time, "s"

"""
rootDirectory = "testSingle"
dataModel = createDataSingleLevel(2,rootDirectory)
dataModel.createData("Arts")
"""