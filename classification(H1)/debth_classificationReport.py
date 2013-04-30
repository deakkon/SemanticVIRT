import os, csv, operator, glob, matplotlib, sys, MySQLdb, gc, sklearn, pp, time
from docutils.utils import uniq
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#functionality
#get list of subdirectories of path
"""
Get number of tokens per category per level
"""
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

def uniq(inlist, indeks):
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
    name = "testData/%s/%s.png" %(model,name)
    plt.savefig(name)

def analyzeSummary(groupingType, model="0.1"):
    """
    Make graphs from summary files: input 
    CSV summary structure: 
        "Category","Level","Model","docsInModel","ReturnedDocsForModel","NrInputDocs"
    """
    path = "testData/%s/%s/summary_100.csv" %(groupingType,model)
    labels = []
    categories = uniq(path, 0)
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

def getMainCat():
    #get root categories to be used
    sqlMainCategories = "select distinct(Title) from dmoz_categories where dmoz_categories.categoryDepth = 1 and dmoz_categories.filterOut = 0"
    mainCatRS = dbQuery(sqlMainCategories)
    mainCat = tuple([x[0] for x in mainCatRS])
    return mainCat

def analyzeCSV(groupingType, model, type=2, analysisType="3",limit = "100"):
    """
    Parameters.
        model :  model to analyize
        type:    type: 1 -> single level sim analysis
                       2 -> range analysis
    
    Get all sim files in model
    iterate over categories
    Distinguish between sngle and range sim files
    Get top n row from sim file, n = numer of items searched for
    Calculate IR measures
    
    
    """
    keys = ['category', 'depth','idLevel','ocID','sim','nrOcc']
    path = "testData/%s/%s/sim/SummaryCSV/%s/" %(groupingType,model,limit)
    categories = getMainCat()
    
    for cat in categories:
        if type==1:
            sysOutFile = path+cat+".txt"
        else:
            sysOutFile = path+cat+"_Range.txt"
            
        sys.stdout = open(sysOutFile, 'wb')
        #get cat debth
        sqlmaxDepth = "select max(categoryDepth) from dmoz_categories where Topic like 'Top/"+str(cat)+"/%' and filterOut = 0"
        maxDebthRS = dbQuery(sqlmaxDepth)
        maxDebth = maxDebthRS[0]
        maxDebth = maxDebth[0]
        ranger = [x for x in range(2,maxDebth+1)]
        print "Category: ", cat
        for level in ranger:
            
            if type == 1:
                fileName = "%s%s_%s_%s.csv" % (path,model,cat,level)
                originalIDFile = "%s%s_%s_%s_original.csv" % (path,model,cat,level) 
            elif type == 2:
                fileName = "%s%s_%s_1_%s.csv" % (path,model,cat,level)
                originalIDFile = "%s%s_%s_1_%s_original.csv" % (path,model,cat,level)
            
            #original categories from sim csv or oid csv 
            if os.path.isfile(originalIDFile):
                nrUID = uniq(originalIDFile, 0)
            else:                
                nrUID = uniq(fileName, 2)
            
            nrUID = [int(i) for i in nrUID]
            #print fileName
            returnedID = uniq(fileName, 3)
            returnedID = [int(i) for i in returnedID[:len(nrUID)]]
            print "level: ", level,"\t",fileName
            #print nrUID
            #print returnedID
            print len(nrUID)
            print len(returnedID)
            if len(nrUID) ==len(returnedID): 
                print sklearn.metrics.classification_report(nrUID,returnedID)
            
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
    
    jobs = [(input, job_server.submit(analyzeCSV, (input,), depfuncs = (dbQuery, errorMessage, returnDirectoryList, removePunct, removeStopWords, getMainCat, calculateSimilarity, prepareComparisonDocuments,getOriginalRowFromModel,), modules = ("sys", "os", "glob", "itertools", "csv","gensim.corpora","gensim.models","gensim.similarities","pp", "time", "MySQLdb","nltk","re","nltk.corpus","nltk.stem","string","gc","urlparse","logging",))) for input in inputs]    
    
    for input, job in jobs:
        job()
    #prints
    job_server.print_stats()
    print "Time elapsed: ", time.time() - start_time, "s"    
    
def updateParallel():
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
    inputs = getMainCat()
    jobs = []
    
    jobs = [(input, job_server.submit(updateEP, (input,), depfuncs = (dbQuery,), modules = ("sys", "os", "glob", "itertools", "csv","gensim.corpora","gensim.models","gensim.similarities","pp", "time", "MySQLdb","nltk","re","nltk.corpus","nltk.stem","string","gc","urlparse","logging",))) for input in inputs]    
    
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
        print analyzeCSV.__doc__
        analyzeCSV("0.1")
    elif var == "3":
        print analyzeCSVPP.__doc__
        analyzeCSVPP()
    elif var == "4":
        print updateCategory.__doc__
        updateCategory()
    elif var == "5":
        print updateParallel.__doc__
        updateParallel()
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        
if __name__ == '__main__':    
    main()