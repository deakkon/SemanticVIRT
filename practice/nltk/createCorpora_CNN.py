import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","","pattern" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
sqlCat = "select distinct `category` from `datahistory`"
try:
    cursor.execute(sqlCat)
    results = cursor.fetchall()
    for row in results:
        catName ='CAT_'
        catName += row[0]
        catName += '.txt'
        sqlCatFile = "select `RECNO`,`userID`,`sessionID`,`URL`,`content`,`category` from `datahistory` where category ='"
        sqlCatFile+=row[0]
        sqlCatFile+="'"
        #print sqlCatFile
        try:
            cursor.execute(sqlCatFile)
            resultsCat = cursor.fetchall()
            kategorija = []
            for row in resultsCat:                
                #destinacija = "\\nltk_data\\"
                ime = ""
                recno = str(row[0])
                userID = row[1]
                sessionID = row[2]
                URL = row[3]
                content = row[4]
                category = row[5]        
                #print recno, userID, sessionID, URL, content,category
                ime += userID
                ime +='#'
                #ime +=sessionID
                ime +='$'
                ime +=recno
                ime +='_'
                ime +=category
                ime +='.txt'
                #destinacija += ime 
                #print destinacija
                FILE = open(ime,"w")
                FILE = open(ime,"w")
                FILE.writelines(content)
                FILE.close()
                #print ime
                imeNL = ime+'\n'
                kategorija.append(imeNL)        
        except MySQLdb.Error, e:
            print "Error " % (e.args[0], e.args[1])
        #destinacija1 = "\\nltk_data\\"
        #destinacija1 +=  catName
        #print destinacija1
        FILE = open(catName,"w")
        FILE.writelines(kategorija)
        FILE.close()    
except MySQLdb.Error, e:
    print "Error " % (e.args[0], e.args[1])        
# execute SQL query using execute() method.
sql = "select `RECNO`,`userID`,`sessionID`,`URL`,`content`,`category` from `datahistory` where `content`!= '' and content != '-'"

# disconnect from server
db.close()