import os, csv, operator, glob, sys, MySQLdb, gc, sklearn.metrics, pp, time
import matplotlib.pyplot as plt
import pygal

#import user defined functions
from sys import path
path.append("/home/jseva/SemanticVIRT/python/utils/")
from databaseODP import dbQuery, truncateTable
from utils import *

def updateCategory():
    """
    Update dmoz_categories; added new field, mainCategory, for further processing speedUp
    """
    categories = getMainCat()
    for category in categories:
        sqlUpdate = "UPDATE dmoz_categories set mainCategory = '"+category+"' where Topic like 'Top/"+str(category)+"/%' and filterOut = '0'"
        print sqlUpdate
        dbQuery(sqlUpdate)

def updateEP(category):
    """
    Update dmoz_categories; added new field, mainCategory, for further processing speedUp
    """
    #catSqlID   ="select catid, mainCategory, fatherid, categoryDepth from dmoz_categories where filterOut = 0 and mainCategory = '%s'" %(category)
    carSQL1 = "select catid, mainCategory, fatherid, categoryDepth from dmoz_categories where filterOut = 0 and categoryDepth = 1"
    catSqlIDData = dbQuery(carSQL1)
    
    for row in catSqlIDData:
        sqlUpdate = "update dmoz_combined set mainCategory= '%s', fatherid= '%s', categoryDepth= '%s', filterOut = '0' where catid= '%s'" %(row[1],row[2],row[3],row[0])
        dbQuery(sqlUpdate)

def getIR_Measures(groupingType, model, category, limit, type):
    """
    Parameters: (groupingType, model, category, limit, type):
        type:   1 -> level results
                2 -> range results

    Steps:
        Get all sim files in model
        iterate over categories
        Distinguish between sngle and range sim files
        Get top n row from sim file, n = numer of items searched for
        Return 3 IR measures: precision, recall, F1 for (groupingType, model, category, limit)
        create single file for category, with structure: 
                filename:categroy.csv
                modelLevel,precision,recall,F1
    """
    
    keys = ['category', 'depth','idLevel','ocID','sim','nrOcc']
    path = "testData_classificationModels/%s/%s/sim/SummaryCSV/%s/" %(groupingType,model,limit)
    
    #range data
    categoryPrecision = []
    categoryRecall = []
    categoryF1 = []    
    
    #get cat debth
    sqlmaxDepth = "select max(categoryDepth) from dmoz_combined where mainCategory = '%s' and filterOut = 0" %(category)
    maxDebthRS = dbQuery(sqlmaxDepth)
    maxDebth = maxDebthRS[0]
    maxDebth = maxDebth[0]
    ranger = [x for x in range(2,maxDebth+1)]
    for level in ranger:
        if type == 1:
            simFile = "%s%s_%s_%s.csv" % (path,model,category,level)
            originalID = "%s%s_%s_%s_original.csv" % (path,model,category,level)
        elif type == 2:
            simFile = "%s%s_%s_1_%s.csv" % (path,model,category,level)
            originalID = "%s%s_%s_1_%s_original.csv" % (path,model,category,level)
        
        #original categories from sim csv or oid csv 
        nrUID = getUniqueItems(originalID, 0)
        returnedID = getUniqueItems(simFile, 3)

        nrUID = [int(i) for i in nrUID]
        returnedID = [int(i) for i in returnedID[:len(nrUID)]]


        if len(returnedID) == 0:
            precision = 0
            recall = 0
            F1 = 0
        else:
            if len(returnedRelative) < len(nrUID):
                for i in range(len(returnedRelative),len(nrUID)):
                    returnedRelative.append(0)
            
            precision = sklearn.metrics.precision_score(nrUID, returnedRelative)
            recall = sklearn.metrics.recall_score(nrUID, returnedRelative)
            F1 = sklearn.metrics.f1_score(nrUID, returnedRelative)
    
        categoryPrecision.append(precision)
        categoryRecall.append(recall)
        categoryF1.append(F1)

    print "Precision\t", categoryPrecision
    print "Recall\t", categoryRecall
    print "F1\t", categoryF1
        
def getIR_Relative_Measures(category, groupingType,limit, model, type):

    path = "testData_classificationModels/%s/%s/sim/SummaryCSV/%s/" %(groupingType,model,limit)    
    categoryPrecision = []
    categoryRecall = []
    categoryF1 = []
    
    #get cat debth
    sqlmaxDepth = "select max(categoryDepth) from dmoz_combined where mainCategory = '%s' and filterOut = 0" %(category)
    maxDebthRS = dbQuery(sqlmaxDepth)
    maxDebth = maxDebthRS[0]
    ranger = [x for x in range(2,maxDebth+1)]
    
    for level in ranger:
        if type == 1:
            simRelative = "%s%s_%s_%s_relative.csv" % (path,model,category,level)
            originalIDFile = "%s%s_%s_%s_original.csv" % (path,model,category,level)
        elif type == 2:
            simRelative = "%s%s_%s_1_%s_relative.csv" % (path,model,category,level)
            originalIDFile = "%s%s_%s_1_%s_original.csv" % (path,model,category,level)
        
        #print "simRelative: %s" %(simRelative)
        #print "originalID: %s" %(originalID)
        
        #original categories from sim csv or oid csv 
        originalID = getCSV_Colmn(originalIDFile, 0)
        returnedRelative = getCSV_Colmn(simRelative, 0)
        returnedRelativeValue = getCSV_Colmn(simRelative, 1)
        returnedRelativeArray = []
        originalID = [int(i) for i in originalID]

        for id, value in zip(returnedRelative,returnedRelativeValue):
            if float(value) > 0:
                returnedRelativeArray.append(int(id))

        if len(returnedRelativeArray) == 0:
            precision = 0.0
            recall = 0.0
            F1 = 0.0

        elif len(returnedRelativeArray) < len(originalID):
            for i in range(len(returnedRelativeArray),len(originalID)):
                returnedRelativeArray.append(0)

            precision = sklearn.metrics.precision_score(originalID, returnedRelativeArray, pos_label=originalID[0])
            recall = sklearn.metrics.recall_score(originalID, returnedRelativeArray, pos_label=originalID[0])
            F1 = sklearn.metrics.f1_score(originalID, returnedRelativeArray, pos_label=originalID[0])
        else:
            precision = sklearn.metrics.precision_score(originalID, returnedRelativeArray[:len(originalID)], pos_label=originalID[0])
            recall = sklearn.metrics.recall_score(originalID, returnedRelativeArray[:len(originalID)], pos_label=originalID[0])
            F1 = sklearn.metrics.f1_score(originalID, returnedRelativeArray[:len(originalID)], pos_label=originalID[0])

        #level based data for category 
        categoryPrecision.append(precision)
        categoryRecall.append(recall)
        categoryF1.append(F1)
    return (categoryPrecision, categoryRecall, categoryF1)
    
        
def calculateMeasures(truncate=False):
    """
    Write analysis results to database
    """
    
    if truncate:
        truncateTable()
        
    range = [1,2]
    
    for type in range:

        limitCategoryPrecision = []
        limitCategoryRecall = []
        limitCategoryF1 = []
        
        GROUPTYPE = ["CATID","FATHERID","GENERAL"]
        models = [0.1, 0.25, 0.5, 0.75, 1.0]
        limits = [10,100,1000]
        
        categories = getMainCat()
        
        for category in categories:
            for groupingType in GROUPTYPE:
                for limit in limits:
                    for model in models:
                        print category, groupingType,limit, model, type
                        #print getIR_Relative_Measures(category, groupingType,limit, model, type)
                        p,r,f1 = getIR_Relative_Measures(category, groupingType,limit, model, type)
                        
                        a = 2
                        for row in p:
                            sqlUpdateP = "INSERT INTO analysis_precision (category, groupingType, limitValue, model, value, levelDepth, typeValue) values ('%s','%s','%s','%s','%s','%i','%s')" %(category,groupingType,limit,model, row, a,type)
                            dbQuery(sqlUpdateP)
                            a += 1
    
                        b = 2
                        for row in r:
                            sqlUpdateR = "INSERT INTO analysis_recall (category, groupingType, limitValue, model, value, levelDepth, typeValue) values ('%s','%s','%s','%s','%s','%i','%s')" %(category,groupingType,limit,model, row, b,type)
                            dbQuery(sqlUpdateR)
                            b += 1
                        
                        c = 2
                        for row in f1:
                            sqlUpdateF1 = "INSERT INTO analysis_f1 (category, groupingType, limitValue, model, value, levelDepth, typeValue) values ('%s','%s','%s','%s','%s','%i','%s')" %(category,groupingType,limit,model, row, c,type)
                            dbQuery(sqlUpdateF1)
                            c += 1

#PARALELL PYTHON
def analyzeCSVPP():
    """
    Paralell Python analisys of sim files
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
    
    # The following submits a job for each category
    inputs = ['0.1','0.25', '0.5', '0.75', '1.0']
    jobs = []
    
    jobs = [(input, job_server.submit(getIR_Measures, (input,), depfuncs = (dbQuery, errorMessage, returnDirectoryList, removePunct, removeStopWords, getMainCat, calculateSimilarity, prepareComparisonDocuments,getOriginalRowFromModel,), modules = ("sys", "os", "glob", "itertools", "csv","gensim.corpora","gensim.models","gensim.similarities","pp", "time", "MySQLdb","nltk","re","nltk.corpus","nltk.stem","string","gc","urlparse","logging",))) for input in inputs]    
    
    for input, job in jobs:
        job()   
    #prints
    job_server.print_stats()
    print "Time elapsed: ", time.time() - start_time, "s"
    
#main UI
def main():
    """
    Functions:
            1. analyzeSummary(model="0.1")
            2. analyzeCSV(model, type=1)
            3. analyzeCSVPP
            4. updateCategory
            5. updateParallel
            
            Anything else to stop
     """
    print main.__doc__

    var = raw_input("Choose function: ")
        
    if var == "1":
        print analyzeSummary.__doc__
        testData = ['0.1','0.25', '0.5', '0.75', '1.0']
        for item in testData:
            analyzeSummary(item)
    elif var == "2":
        print getIR_Measures.__doc__
        getIR_Measures("FATHERID", 1.0 , "Arts", 10, 2)
    elif var == "3":
        print analyzeCSVPP.__doc__
        analyzeCSVPP()
    elif var == "4":
        print updateCategory.__doc__
        updateCategory()
    elif var == "5":
        print updateParallel.__doc__
        updateParallel()
    elif var == "6":
        print calculateMeasures.__doc__
        calculateMeasures(True)
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        
if __name__ == '__main__':    
    main()
    
    
    