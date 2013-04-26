import MySQLdb, sys

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