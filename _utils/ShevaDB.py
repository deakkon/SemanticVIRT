#imports
import MySQLdb 
import sys
import random
#import redis

#USER DEFINED MODULES
#sys.path.append("/home/jseva/SemanticVIRT/_utils/")
#from ShevaCSV import ShevaCSV

class ShevaDB:
    def __init__(self):
        self.host= "localhost"
        self.user= "root"
        self.passwd = "root"
        self.database= "dmoz"
    
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
        #get sample size
        #print "CS:",corpusSize
        sampleSize = int((testSize * corpusSize)/100)
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
        print dbData
        for item in dbData:
            print item

        categoryDataOID = [str(item[1]) for item in dbData]
        dbData=[item[0].split() for item in dbData]

        return (categoryDataOID,dbData)
