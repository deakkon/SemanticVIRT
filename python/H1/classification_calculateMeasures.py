import os, csv, operator, glob, matplotlib, sys, MySQLdb, gc, sklearn.metrics, pp, time
from numpy.lib.function_base import append
from sqlalchemy.sql.expression import except_
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pygal


#functionality
def dbQuery(sql):

    try:
        gc.collect()
        con = MySQLdb.connect(host="localhost", user="root", passwd="root", db="dmoz")
        con.autocommit(True)
    
    except MySQLdb.Error, e:
        print "Error dbConnect %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
        
    try:
        cur = con.cursor()
        cur.execute(sql) 
        numrows = int(cur.rowcount)
        if numrows == 1:
            resultRows =  [cur.fetchone()]
        elif numrows > 1: 
            resultRows = [x for x in cur.fetchall()]
        else: 
            resultRows = 0
        cur.close()
        con.close()
        return resultRows
    
    except MySQLdb.Error, e:
        print "Error dbQuery %d: %s" % (e.args[0],e.args[1])
        print "Erroneous query: ",sql
        sys.exit(1) 
        
def getMainCat():
    """
    Returns main categories from ODP; input for PP pipeline
    """
    sqlMainCategories = "select distinct(Title) from dmoz_categories where dmoz_categories.categoryDepth = 1 and dmoz_categories.filterOut = 0"
    mainCatRS = dbQuery(sqlMainCategories)
    mainCat = tuple([x[0] for x in mainCatRS])
    return mainCat

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

def returnDirectoryList(path):
    directories = []
    
    for files in os.listdir(path): 
        if os.path.isdir(os.path.join(path,files)):
            #print "Directory : ",files
            directories.append(files)
    return directories

#get unique fileds in csv, ignore header line

def getUniqueItems(inlist, indeks=""):
    """
    Return uniqe values from column indeks from either list or csv file inlist
    """
    #variables
    uniques = []
    rownum = 0
    
    if type(inlist) is str:
        f = open(inlist, "rb") # don't forget the 'b'!
        inlist = csv.reader(f)
    
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

def getCSV_Colmn(file,column):
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

def getMainCat():
    #get root categories to be used
    sqlMainCategories = "select distinct(Title) from dmoz_categories where dmoz_categories.categoryDepth = 1 and dmoz_categories.filterOut = 0"
    mainCatRS = dbQuery(sqlMainCategories)
    mainCat = tuple([x[0] for x in mainCatRS])
    return mainCat

def computeClassificationMetrics(y_true,y_pred):
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    F1 = f1_score(y_true, y_pred)
    return (precision,recall, F1)

#graphing functions

def summaryGraph(a,b,labels,name,model):
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

def analyzeSummary(groupingType, model, limit):
    """
    Make graphs from summary files: input 
    CSV summary structure: 
        "Category","Level","Model","docsInModel","ReturnedDocsForModel","NrInputDocs"
    """
    path = "testData_classificationModels/%s/%s/summary_%s.csv" %(groupingType,model,limit)
    labels = []
    categories = getUniqueItems(path, 0)
    plt.rc('legend',**{'fontsize':6})
    
    contentSingleDocsInModel = []
    contentSingleReturnedDocs= []
    
    contentRangeDocsInModel= []
    contentRangeReturnedDocs= []
    rangeLabels = []

    #graphs for summary
    for cat in categories: 
        content = []
        #range data
        f = open(path, "rb")
        reader = csv.reader(f)
        contentRange = [row for row in reader if row[0] == cat and row[2].count('_') == 3]
        
        tempRangeDocsInModel = [int(x[3]) for x in contentRange]
        tempRangerangeReturnedDocsForModel = [int(x[4]) for x in contentRange]
        f.close()
        
        #single data
        f = open(path, "rb") # don't forget the 'b'!
        reader = csv.reader(f)
        contentSingle = [row for row in reader if row[0] == cat and row[2].count('_') == 2]
        #values
        singleDocsInModel = [int(x[3]) for x in contentSingle]
        singleReturnedDocsForModel = [int(x[4]) for x in contentSingle]
        
        position = len(singleDocsInModel) + 1
        
        while position < 14:
            singleDocsInModel.insert(position,0)
            singleReturnedDocsForModel.insert(position,0)
            tempRangeDocsInModel.insert(position,0)
            tempRangerangeReturnedDocsForModel.insert(position,0)
            position += 1
        
        
        #single model
        contentSingleDocsInModel.append(singleDocsInModel)
        contentSingleReturnedDocs.append(singleReturnedDocsForModel)
        
        #range model
        contentRangeDocsInModel.append(tempRangeDocsInModel)
        contentRangeReturnedDocs.append(tempRangerangeReturnedDocsForModel)
        f.close()
       
        #labels
        labels.append(cat)
        
    #print contentSingleDocsInModel
    #print contentSingleReturnedDocs
    summaryGraph(contentSingleDocsInModel, contentSingleReturnedDocs,labels, "single",model)
    summaryGraph(contentRangeDocsInModel, contentRangeReturnedDocs,labels, "range", model)

#open csv for reading

def analyzeRelative():
    pass

def createCSV(filename,data):
    """
    Creates filename.csv based on data, either list of cictionary
    """

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

    #GROUPTYPE = ["CATID","FATHERID","GENERAL"]
    #models = [0.1, 0.25, 0.5, 0.75, 1.0]
    #limits = [10,100,1000]
    
    relativeResultsFile = "testData_classificationModels/relativeResultsFile.csv"
    
    #for groupingType in GROUPTYPE:
        
        #limitCategoryPrecision = []
        #limitCategoryRecall = []
        #limitCategoryF1 = []
        #for limit in limits:
            #for model in models:
                #range data
    limitCategoryPrecision = []
    limitCategoryRecall = []
    limitCategoryF1 = []

    #print category, groupingType, model, limit, type

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
            simRelative = "%s%s_%s_%s_relative.csv" % (path,model,category,level)
            originalID = "%s%s_%s_%s_original.csv" % (path,model,category,level)
            saveEnd = "_level.jpg"
        elif type == 2:
            simRelative = "%s%s_%s_1_%s_relative.csv" % (path,model,category,level)
            originalID = "%s%s_%s_1_%s_original.csv" % (path,model,category,level)
            saveEnd = "_range.jpg"
        
        #print "simRelative: %s" %(simRelative)
        #print "originalID: %s" %(originalID)

        #original categories from sim csv or oid csv 
        nrUID = getUniqueItems(originalID, 0)
        returnedRelative = getCSV_Colmn(simRelative, 0)
        returnedRelativeValue = getCSV_Colmn(simRelative, 1)
        returnedRelativeArray = []
        
        nrUID = [int(i) for i in nrUID]
        #print "nrUID: %s" %(nrUID)
        #print "returnedRelative: %s" %(returnedRelative)
        #print "returnedRelativeValue: %s" %(returnedRelativeValue)
        
        for id, value in zip(returnedRelative,returnedRelativeValue):
            #print id, value
            if value != 0.0 or value != 0:
                returnedRelativeArray.append(int(id))
        
        if len(returnedRelativeArray) == 0:
            precision = 0.0
            recall = 0.0
            F1 = 0.0
        elif len(returnedRelativeArray) < len(nrUID):
            for i in range(len(returnedRelativeArray),len(nrUID)):
                returnedRelativeArray.append(0)

            precision = sklearn.metrics.precision_score(nrUID, returnedRelativeArray, pos_label=nrUID[0], average='macro')
            recall = sklearn.metrics.recall_score(nrUID, returnedRelativeArray, pos_label=nrUID[0], average='macro')
            F1 = sklearn.metrics.f1_score(nrUID, returnedRelativeArray, pos_label=nrUID[0], average='macro')
        else:
            precision = sklearn.metrics.precision_score(nrUID, returnedRelativeArray[:len(nrUID)], pos_label=nrUID[0], average='macro')
            recall = sklearn.metrics.recall_score(nrUID, returnedRelativeArray[:len(nrUID)], pos_label=nrUID[0], average='macro')
            F1 = sklearn.metrics.f1_score(nrUID, returnedRelativeArray[:len(nrUID)], pos_label=nrUID[0], average='macro')        

        #level based data for category 
        categoryPrecision.append(precision)
        categoryRecall.append(recall)
        categoryF1.append(F1)
    return (categoryPrecision, categoryRecall, categoryF1)

def truncateTable():
    tables = ["analysis_f1","analysis_precision","analysis_recall"]
    for table in tables: 
        sql = "TRUNCATE TABLE  %s" %(table)
        dbQuery(sql)
        
def calculateMeasures(truncate=False):
    """
    testing plotting 
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
    
    
    