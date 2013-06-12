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

#PYTHON MODULES
import math
import time
import csv
import os
import string
import pp
import re
import itertools
import gc

class createDataLimit:
    
    def __init__(self,type,rootDir):
        """
        type: 1 -> full data
              2 -> limited data
        """

        #percentage of data to be used for model build
        if type == 1:
            self.GROUPTYPE = ["CATID", "FATHERID", "GENERAL"]
            self.percentageList = [1000, 2500, 5000, 7500, 10000, 20000]
        elif type == 2:
            self.GROUPTYPE = ["GENERAL"]
            self.percentageList = [1000]
        else:
            sys.exit("Wrong 'type' parameter in createData.__init__")
        
        self.shevaDB = ShevaDB()
        self.shevaTPF = ShevaTPF()
        self.shevaUtils = ShevaUtils()
        self.shevaVect = ShevaVect()
        
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

        for group in self.GROUPTYPE:
            
            #gruping dependent queries
            if group != "FATHERID":
                sqlCategory = "select Description, catid from dmoz_combined where mainCategory = '%s' limit 20000" %(category)
            else:
                sqlCategory = "select Description, fatherid from dmoz_combined where mainCategory = '%s' limit 20000" %(category)
            
            sqlQueryResults = self.shevaDB.dbQuery(sqlCategory)
            
            if sqlQueryResults == 0:
                sys.exit("SQL code error in level: \t", category,"\t",indeks,"\t",sqlCategoryLevel)

            for percentageItem in self.percentageList:
                sqlQueryResultsLimit = [x for x in sqlQueryResults[:percentageItem]]
                #data for % model, range data
                dataCategoryLevelAll = []
                dataCategoryLabelAll = []
                originalCatIDAll = []
                dataCategorySingleAll = []
                
                path = "%s/%s/%s/" %(self.rootDir,group,percentageItem)
                self.shevaUtils.createDir(self.rootDir,group,percentageItem)
                
                #for indeks in ranger:
                #level list variables
                dataCategoryLevel = []
                dataCategoryLabel = []
                originalCatID = []
                originalFatherID = []
                finalContent = []
                    
                #get unique values
                if group == "GENERAL":
                    finalContent = [[item for item in row[0].split()] for row in sqlQueryResultsLimit]
                    originalCatID = [row[1] for row in sqlQueryResultsLimit]
                    dataCategoryLevel.extend(self.shevaTPF.returnClean(finalContent,1))
                else:
                    unique = []
                    for row in sqlQueryResultsLimit:
                        if row[1] not in unique:
                            unique.append(row[1])

                    #prepare rows with uniq for document in model
                    for uniq in unique:
                        tempUnique = []
                        tempUnique = [row[0].split() for row in sqlQueryResultsLimit if row[1] == uniq]
                        mergedContent = [i for i in itertools.chain.from_iterable(tempUnique)]
                        finalContent.append(mergedContent)
                        originalCatID.append(uniq)
                    dataCategoryLevel.extend(self.shevaTPF.returnClean(finalContent,1))

                self.shevaUtils.createDir(self.rootDir, group, percentageItem)

                #create file names
                #fileNameAll = "%s_%s_1_%s" %(str(percentageItem),category,str(indeks))
                fileNameLevel = "%s_%s" %(str(percentageItem),category)
                fileNameSingleAll = "%s_%s_single" %(str(percentageItem),category)
    
                ##########   ORIGINAL DESCRIPTION AND VECTORIZATION  #################
                #create corpus models
                self.shevaVect.createCorpusAndVectorModel(dataCategoryLevel,fileNameLevel,path)
                #dataCategoryLevelAll.extend(dataCategoryLevel)
                #self.shevaVect.createCorpusAndVectorModel(dataCategoryLevelAll, fileNameAll,path)

                #single model for all documents
                #dataCategorySingleAll.append([x for sublist in dataCategoryLevelAll for x in sublist])
                #createCorpusAndVectorModel(dataCategorySingleAll, percentageItem, fileName=fileNameSingleAll)
    
                ##########   ORIGINAL CATEGORIES ID   #################
                self.shevaUtils.getCategoryListLevel(originalCatID,fileNameLevel,path)
                #originalCatIDAll.extend(originalCatID)
                #self.shevaUtils.getCategoryListLevel(originalCatIDAll,fileNameAll,path)
                
                #print out number of documents for (cat,level,model)
                print "Done with:\t",group,"\t",category,"\t","\t",percentageItem
                #######################    LABEL    #################

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
    dataModel = createDataLimit(1,rootDirectory)
    print dataModel.GROUPTYPE
    print dataModel.percentageList
    print dataModel.rootDir
    jobs.append(job_server.submit(dataModel.createData, 
                                  (index,),
                                  depfuncs = (),
                                  modules = ("time","ShevaCreateLimitModels","ShevaDB","ShevaTPF","ShevaUtils","ShevaVect","gc","itertools",)))

for job in jobs:
    result = job()
    if result:
        break
#prints
job_server.print_stats()
print "Time elapsed: ", time.time() - start_time, "s"
