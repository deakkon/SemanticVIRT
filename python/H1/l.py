import MySQLdb, sys, pp, time

def dbQuery(sql):

    try:
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
            resultRows = cur.fetchone()
        elif numrows > 1: 
            resultRows = cur.fetchall()
        else: 
            resultRows = 0        
        return resultRows
        cur.close()
        con.close()
        
    
    except MySQLdb.Error, e:
        print "Error dbQuery %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
        
def getMainCat():
    #get root categories to be used
    sqlMainCategories = "select distinct(Title) from dmoz_categories where dmoz_categories.categoryDepth = 1 and dmoz_categories.filterOut = 0"
    mainCatRS = dbQuery(sqlMainCategories)
    mainCat = tuple([x[0] for x in mainCatRS])
    return mainCat        
        
def createData():
    
    """
    1. get root categories to be used and iterate through main categories
    3. get max depth for individual category
    4. from 1 to max till 1 to 1
        get all catid for iterated category
        get all pages for selected categories
        call createCorpusAndVectorModel fro selected documents
    """
    #percentage of data to be used for model build
    testData = ['0.75', '0.5', '1.0', '0.1', '0.25']
    
    categories = getMainCat()
    
    for category in categories:
        #get max debth
        sqlmaxDepth = "select max(categoryDepth) from dmoz_categories where Topic like 'Top/"+str(category)+"/%' and filterOut = 0"
        maxDebthRS = dbQuery(sqlmaxDepth)
        maxDebth = maxDebthRS[0]
        #print maxDebth
        #maxDebth = 3
        
        #(1,indeks) list variables
        dataCategoryLevelAll = []
        dataCategoryLabelAll = []
        originalCatIDAll = []
        dataCategorySingleAll = []
        #counter
        indeks = 2
    
        #go through all levels (2,maxDebth)
        while indeks <= maxDebth:
            #dynamic SQL queries
            #print indeks
            sqlCategoryLevel = "select Description,Title,link,catid from dmoz_externalpages where filterOut = 0 and catid in (select catid from dmoz_categories where Topic like 'Top/"+category+"/%' and categoryDepth = "+str(indeks)+" and filterOut = 0) limit 100"            
            sqlCategoryLabel = "select distinct(Title) from dmoz_categories where Topic like 'Top/"+category+"/%' and categoryDepth = "+str(indeks)+ " and filterOut = 0"
    
            #getData
            sqlQueryResultsLevel = dbQuery(sqlCategoryLevel)
            sqlQueryResultsLabel = dbQuery(sqlCategoryLabel)
            
            #print len(sqlCategoryLevel),"    ",sqlCategoryLevel
            #print len(sqlCategoryLabel),"    ",sqlCategoryLabel  
            
            #print out
            if len(sqlCategoryLevel) == 0:                
                print category,"    ",indeks,"    ",len(sqlCategoryLevel),"    ",sqlCategoryLevel
            if len(sqlCategoryLabel) == 0:            
                print category,"    ",indeks,"    ",len(sqlCategoryLabel),"    ",sqlCategoryLabel
            indeks +=1
            
#run PP
def runParallelCategory():
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
    
    # The following submits a job for each category
    inputs = getMainCat()
    #inputs =("Arts",)
    
    jobs = []
    
    for index in inputs:
        #print index
        jobs.append(job_server.submit(createData, (index,), depfuncs = (dbQuery, getMainCat, ), modules = ("MySQLdb","sys","pp","time",)))    
    for job in jobs:
        result = job()
        if result:
            break
    #prints
    job_server.print_stats()
    print "Time elapsed: ", time.time() - start_time, "s"

#main UI

def main():
    """
    Functions:
            1. getMainCat()
            2. prepareComparisonDocuments(sqlQuery)
            3. getFileList(folder)
            4. returnSimilarities(category, compareTo="3", limit = "1000")
            5. runParallelCategory()
            Anything else to stop
     """
    print main.__doc__

    var = raw_input("Choose function: ")
        
    if var == "1":
        print getMainCat.__doc__
        getMainCat()    
    if var == "2":
        print prepareComparisonDocuments.__doc__
        var1 = raw_input("Insert SQL query")
        prepareComparisonDocuments(var1)        
    elif var == "3":
        print getFileList.__doc__
        var1 = raw_input("Folder to list data from (experimental): ")
        getFileList(var1)
    elif var == "4":
        myFile= open( "memAnalyzer.txt", "w", 0) 
        sys.stdout= myFile
        print returnSimilaritiesCategory.__doc__
        returnSimilaritiesCategory("News")
    elif var == "5":
        print runParallelCategory.__doc__
        runParallelCategory()             
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        
if __name__ == '__main__':    
    main()
            