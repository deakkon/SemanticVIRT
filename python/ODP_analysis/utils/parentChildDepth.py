"""
Parent-child analysis for depth level in ODP hierarchy, based on delimiter '/'

"""

import MySQLdb

def calculateDepthTopicUpdate():
    seq = []
    #DB
    con = MySQLdb.connect(host="localhost", user="root", passwd="", db="dmoz_new")
    con.autocommit(True)
    cur = con.cursor()
    #sql = "select Topic from dmoz_categories where Topic != '%World%' and Topic != '%Adult%' limit 1000"
    sql = "select id,Topic, (length(Topic)-length(replace(Topic,'/','')))/length('/') as nR, fatherid, categoryDepth FROM dmoz_categories n where filterOut=0"
    with con:
        cur.execute(sql)
        resultRows = cur.fetchall()
    #print resultRows

    for i in resultRows:
        seq.append([int(i[2]),int(i[0])])    
                 
        #cur = con.cursor()
        #print i, "    ",str(i).count("/")
        #print i[0],"    ",i[1],"                                                                ",int(i[2])
       
        sql = "update dmoz_categories set categoryDepth = '%s' WHERE id = '%s'" % (int(i[2]),int(i[0]))
        try:
            print sql
            cur.execute(sql)
            results = cur.fetchall()
            print results
        except MySQLdb.Error, e:
            print "An error has been passed. %s", e
       
    """
    try:
        cur.executemany("update dmoz_categories set categoryDepth = '%s' WHERE id = '%s'",seq)
        results = cur.fetchall()
        print results
    except MySQLdb.Error, e:
        print "An error has been passed. %s", e
    """
    
    cur.close()
    con.close()