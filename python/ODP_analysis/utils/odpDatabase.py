'''
Created on 4.1.2013.

@author: Jurica Seva

PhD Candidate 
Faculty of Organization and Informatics
University of Zagreb
'''
import MySQLdb, sys

def errorMessage(msg):
    print msg

def dbConnect():
    """
    Basic dB functionality
    COnnect to db, return connection handler
    """
    try:
        db = MySQLdb.connect(host="localhost", user="root", passwd="", db="dmoz_new")
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
    
def dbQuery(con, sql):
    #con = conn.execute(sql)
    #print sql
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
