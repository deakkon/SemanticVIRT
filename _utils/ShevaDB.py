#imports
import MySQLdb 
import sys
import random

class ShevaDB:
    def __init__(self):
        self.host= "localhost"
        self.user= "root"
        self.passwd = "root"
        self.database= "dmoz"
        #print "ShevaDB created"
        
    def __del__(self):
        #print 'ShevaDB destroyed'
        pass
    
    def dbConnect(self):
        try:
            db = MySQLdb.connect(self.host, self.user, self.passwd, self.database)
            db.autocommit(True)
            return db


        except MySQLdb.Error, e:
            print "Error dbConnect %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)

    def dbDisconnect(self,connection):
        connection.close()

    def dbQuery(self,sql):
        con = self.dbConnect()

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
            cur.close()
            self.dbDisconnect(con)
            return resultRows
        
        except MySQLdb.Error, e:
            print "Error dbQuery %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)

    def errorMessage(self,msg):
        print msg
        sys.exit(1)
        
    def truncateTable(self):
        tables = ["analysis_f1","analysis_precision","analysis_recall"]
        for table in tables: 
            sql = "TRUNCATE TABLE  %s" %(table)
            self.dbQuery(sql)

    def getMainCat(self):
        """
        Returns main categories from ODP; input for PP pipeline
        """
        sqlMainCategories = "select distinct(Title) from dmoz_categories where dmoz_categories.categoryDepth = 1 and dmoz_categories.filterOut = 0"
        mainCatRS = self.dbQuery(sqlMainCategories)
        mainCat = tuple([x[0] for x in mainCatRS])
        return mainCat
    
    def getCategoryDepth(self,category):
        depthQuery = "select max(categoryDepth) from dmoz_combined where mainCategory = '%s' and filterOut = 0" %(category)
        maxDebthRS = self.dbQuery(depthQuery)
        #print maxDebthRS, type(maxDebthRS), maxDebthRS[0]
        maxDebth = maxDebthRS[0]
        #maxDebth = int(maxDebth[0])
        ranger = [x for x in range(4,maxDebth+1)]
        return ranger
    
    def getCategorymaxDepth(self,category):
        depthQuery = "select max(categoryDepth) from dmoz_combined where mainCategory = '%s' and filterOut = 0" %(category)
        maxDebthRS = self.dbQuery(depthQuery)
        #print maxDebthRS, type(maxDebthRS), maxDebthRS[0]
        maxDebth = maxDebthRS[0]
        return maxDebth 
    
    def getSimilarityDocuments(self, category, groupType, limit, depth="", level=""):
        """
        Get documents from DB, for classification testing. 
        """
        sqlRandomResults = []
        if depth != "" and level != "":
            sys.exit("Bro, you gotta chose one! ShevaDB.getSimilarityDB_Documents")
        elif depth != "" and level == "":
            sqlRandom = "SELECT Description, catid, fatherid from dmoz_combined where mainCategory = '%s' and categoryDepth = '%s'" %(category,depth)
        elif level != "" and depth == "":
            sqlRandom = "SELECT Description, catid, fatherid from dmoz_combined where mainCategory = '%s' limit '%s'" %(category,level)
        else:
            sqlRandom = "SELECT Description, catid, fatherid from dmoz_combined where mainCategory = '%s'"

        sqlResults = self.dbQuery(sqlRandom)

        if sqlResults == 0:
            sys.exit("ShevaDB.getSimilarityDocuments.")

        if len(sqlResults) > int(limit):
            indices = random.sample(xrange(len(sqlResults)), int(limit))
            sqlRandomResults=[sqlResults[i] for i in indices]
        else:
            sqlRandomResults = sqlResults
            
        #different data for different grouping
        if groupingType != "FATHERID":
            randomItems = [operator.itemgetter(0,1)(i) for i in sqlRandomResults]
        else:
            randomItems = [operator.itemgetter(0,2)(i) for i in sqlRandomResults]

        return randomItems
    
    def getDBDocuments(self, category):
        """
        Get ALL documents from category
        """
        
        sqlCategoryDocuments = "SELECT Description, catid, fatherid from dmoz_combined where mainCategory = '%s'" %(category)
        sqlResults = self.dbQuery(sqlCategoryDocuments)
        return sqlResults
    
    def getDBDocumentsDepth(self, category, depth):
        """
        Get ALL documents from category
        """
        
        sqlCategoryDocuments = "SELECT Description, catid, fatherid from dmoz_combined where mainCategory = '%s' and categoryDepth = '%i'" %(category, depth)
        sqlResults = self.dbQuery(sqlCategoryDocuments)
        return sqlResults    
        
    
    def getSampleDocuments(self, category, depth, id, sampleSize):
        """
        Ge all original id's form cat/level and take sample size from them
        return sample documents
        """
        pass
    
    def createREDIS(self):
        r = redis.Redis(host='localhost', port=6379, db=0)
        return r
    
    #@profile
    def getSample(self,corpusSize,testSize,category,debth, group):
        print "started sampling" 
        #get sample size
        #print "CS:",corpusSize
        sampleSize = int((testSize * corpusSize)/100)
        if sampleSize > 10000:
            sampleSize = 10000

        #print "SS:",sampleSize
        if sampleSize == 0:
            sampleSize = 1

        categoryDataOID = []
        #dbData = self.getDBDocumentsDepth(category,debth)
        if group != "FATHERID":
            sqlCategoryDocuments = "SELECT Description, catid from dmoz_combined where mainCategory = '%s' and categoryDepth <= '%i' limit %i" %(category, debth, sampleSize)
        else:
            sqlCategoryDocuments = "SELECT Description, fatherid from dmoz_combined where mainCategory = '%s' and categoryDepth <= '%i' limit %i" %(category, debth, sampleSize)
             
        dbData = self.dbQuery(sqlCategoryDocuments)


        categoryDataOID = [str(item[1]) for item in dbData]
        dbData=[item[0].split() for item in dbData]
        
        print "ended sampling"
        return (categoryDataOID,dbData)
    
    def getSample8020(self,corpusSize,testSize,category,debth, group):
        print "started sampling"
        """
        Take the last 20% of data from selected limit model and return prepared data
        """
        
        categoryDataOID = []
        #dbData = self.getDBDocumentsDepth(category,debth)
        if group != "FATHERID":
            sqlCategoryDocuments = "SELECT Description, catid from dmoz_combined where mainCategory = '%s' and categoryDepth <= '%i' limit %i" %(category, debth, corpusSize)
        else:
            sqlCategoryDocuments = "SELECT Description, fatherid from dmoz_combined where mainCategory = '%s' and categoryDepth <= '%i' limit %i" %(category, debth, corpusSize)
             
        dbData = self.dbQuery(sqlCategoryDocuments)


        categoryDataOID = [str(item[1]) for item in dbData[testSize:]]
        dbData=[item[0].split() for item in dbData[testSize:]]
        
        print "ended sampling"
        return (categoryDataOID,dbData)    

    
    def getSampleLimit(self, category, debth, group, limit):
        print "started sampling" 

        categoryDataOID = []
        #dbData = self.getDBDocumentsDepth(category,debth)
        if group != "FATHERID":
            sqlCategoryDocuments = "SELECT Description, catid from dmoz_combined where mainCategory = '%s' and categoryDepth <= '%i' limit %i" %(category, debth, limit)
        else:
            sqlCategoryDocuments = "SELECT Description, fatherid from dmoz_combined where mainCategory = '%s' and categoryDepth <= '%i' limit %i" %(category, debth, limit)
             
        dbData = self.dbQuery(sqlCategoryDocuments)


        categoryDataOID = [str(item[1]) for item in dbData]
        dbData=[item[0].split() for item in dbData]
        
        print "ended sampling"
        return (categoryDataOID,dbData)    
    
    def getNumberOfRows(self, category, group, limit, depth):
        sqlQuery = "SELECT count(*) from analysis_results where category = '%s' and groupingType = '%s' and limitValue = '%s' and levelDepth = '%s'" %(category, group, limit, depth)        
        dbData = self.dbQuery(sqlQuery)
        #print dbData[0], type(dbData[0])
        return int(dbData[0])
    
    #@profile
    def prepareComparisonDocuments(self, sqlQuery):
        """
        Input: 
            sqlQuery to be executed, first parameter being textual data to convert to BoW
            
        Returns:
            BoW representation of documents returned from sqlQuery, list of lists
        """
        #variables
        originalID = []
        bowReturn = []    
        
        #check sqlQuery
        if sqlQuery == "":
            sys.exit("No query mate @ ShevaLevelSIM.prepareComparisonDocuments()")
        elif type(sqlQuery) is str:
            sqlQueryResults = self.dbQuery(sqlQuery)
        elif type(sqlQuery) is tuple or type(sqlQuery) is list:
            sqlQueryResults = sqlQuery
        else:
            print type(sqlQuery)
            print "Error @ ShevaLevelSIM.prepareComparisonDocuments() "
            sys.exit(1)
            
        content= [[item for item in row[0].split()] for row in sqlQueryResults]
        bowReturn.extend(self.shevaTPF.returnClean(content))
        originalID = [row[1] for row in sqlQueryResults]
        return (bowReturn,originalID)
    
    def getCategoryLabel(self,sqlQuery,fileName):
        """
        sqlQuery -> query to be executed or query result set
        fileName -> file to save labels returned by the query
        """
        #variables
        categoryLabels = []
        
        #default data
        if sqlQuery == "":
            sys.exit("No query mate. Function getCategoryLabel")
        elif type(sqlQuery) is str:
            sqlQueryResults = ShevaDB().dbQuery(sqlQuery)
        elif type(sqlQuery) is tuple:
            sqlQueryResults = sqlQuery
        else:
            print type(sqlQuery)
            print "error createVectorModel getCategoryLabel "
            sys.exit(1)
        
        #print executed query
        #print sqlQuery
            
        #iteration through documents   
        for row in sqlQueryResults:
            if type(row) is not long:
                #print type(row)," :: ",type(row[0]), row[0]
                #missing: remove stop words, punctuation, names
                categoryLabels.append(removeStopWords(row[0]))   
                #categoryLabels.append(str(row[0]))
            
        #print sqlQueryResults
        #categoryLabels = [row[0] for row in sqlQueryResults]
        #print categoryLabels
        """
        dictionary = corpora.Dictionary(categoryLabels)
        dictFN = "labels/"+fileName+".dict"
        dictionary.save(dictFN)
        """
    
        #path to save the file    
        if os.path.realpath(__file__)== "/home/jseva/SemanticVIRT/python/utils/createVectorModel.py":
            fileName = "../H1/labels/"+fileName+".csv"
        else:
            fileName = "labels/"+fileName+".csv"    
        
        out = csv.writer(open(fileName,"w"), delimiter=',',quoting=csv.QUOTE_ALL)
        
        writeLabels = []
        #append to file
        print string.letters
        for row in categoryLabels:
            print row
            #print type(row)
            #print len(row)
            for i in row:            
                if i != "" or i.lower() not in string.letters.lower():
                    #print i.lower()
                    #out.writerow(i)
                    writeLabels.append(i.lower())
        print writeLabels
        out.writerow(writeLabels)
        #return categoryLabels 
        
    def returnFatherIDs(self,sqlQuery):
        """
        MOVED TO SHEVADB
        Group catid, on specific depth level,  based on their fatherID values
        sql query -> fatherID first level 
        Returns fatherID on level x    
        """
        #variables
        fatherIDLevel = []
        
        if sqlQuery == "":
            sys.exit("No query mate. Function getCategoryLabel")
        elif type(sqlQuery) is str:
            sqlQueryResults = ShevaDB().dbQuery(sqlQuery)
        elif type(sqlQuery) is tuple:
            sqlQueryResults = sqlQuery
        else:
            print type(sqlQuery)
            print "yaba daba doo createVectorModel getCategoryLabel "
            sys.exit(1)
            
        #iterate through returned
        for row in sqlQueryResults:
            #print row[0]
            fatherIDLevel.append(row[0])
            
        #return values 
        return fatherIDLevel
    
    def getLabels(self,catID):
        originalLables = []
        self.database = "dmoz"
        for item in catID:
            sqlLabel = "select Title from dmoz_categories where catid = %s" %(item)
            result = self.dbQuery(sqlLabel)
            originalLables.append(result[0])
        return originalLables
            