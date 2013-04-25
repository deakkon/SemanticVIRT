'''
Created on 4.1.2013.

@author: Jurica Seva

PhD Candidate 
Faculty of Organization and Informatics
University of Zagreb

Functions:
dbConnect()
dbDisconnect()
dbQuery(sql)
errorMessage(msg)
'''
import MySQLdb, sys

def dbConnect():
    """
    Basic dB functionality
    COnnect to db, return connection handler
    """
    try:
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="dmoz")
        db.autocommit(True)
        return db        
    
    except MySQLdb.Error, e:
        print "Error dbConnect %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
        
def dbConnectRemote():
    """
    Basic dB functionality
    COnnect to db, return connection handler
    """
    try:
        db = MySQLdb.connect(host="xxx.xxx.xxx.xxx", user="xxxxxxx", passwd="xxxxxxx", db="xxxxxxx")
        db.autocommit(True)
        return db        
    
    except MySQLdb.Error, e:
        print "Error dbConnect %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

def dbDisconnect(connection):
    """
    Basic dB functionality
    COnnect to db, return connection handler
    """
    connection.close()
    
def dbQuery(sql):

    con =dbConnect()
    #con = dbConnectRemote()
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
        dbDisconnect(con)
        return resultRows
    
    except MySQLdb.Error, e:
        print "Error dbQuery %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)


def errorMessage(msg):
    print msg
    sys.exit(1)
    
def truncateTable():
    tables = ["analysis_f1","analysis_precision","analysis_recall"]
    for table in tables: 
        sql = "TRUNCATE TABLE  %s" %(table)
        dbQuery(sql)
