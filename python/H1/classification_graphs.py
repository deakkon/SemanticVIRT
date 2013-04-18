import sys 
import MySQLdb
import pygal
import gc
from pygal.style import *

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
        if item[indeks] not in uniques:
            #print item[indeks]
            uniques.append(item[indeks])
    return uniques


def returnAnalysisReuslts(grouping,model,limit,range):
    sqlAnalysisReport = "select * from analysis_precision where groupingType = '%s' and model='%s' and limitValue = '%s' and typeValue = '%s'" %(grouping,model,limit,range)
    analysisReport = dbQuery(sqlAnalysisReport)
    return analysisReport

def prepareData(sqlResults):
    data = []
    labels = getUniqueItems(sqlResults,6)
    categories = getUniqueItems(sqlResults,1)
    for cat in categories:
        catData = []
        catData.append(cat)
        tempdata = [float(x[5]) for x in sqlResults if x[1] == cat]
        catData.extend(tempdata)
        data.append(catData)
    return (data,labels)

def RadarGraph(grouping, model, limit, range):
    """
    title: string
    labels: list
    data: list of lists
    """

    data, labels  = prepareData(returnAnalysisReuslts(grouping,model,limit,range))
    radar_chart = pygal.Radar(x_scale=.1, y_scale=.1, style=LightStyle)
    title = "%s %s %s %s" %(grouping, model, limit, range)
    radar_chart.title = title
    radar_chart.x_labels = labels
    
    for row in data:
        #print row[0], row[1:]
        radar_chart.add(row[0],row[1:])
    
    fn = "graphs/%s_%s_%s_%s.svg" %(grouping, model, limit, range)
    radar_chart.render_to_file(fn)
    print grouping, model, limit, range, fn

def drawRadarGraph():
    GROUPTYPE = ["CATID","FATHERID","GENERAL"]
    models = [0.1, 0.25, 0.5, 0.75, 1.0]
    limits = [10,100,1000]
    ranges = [1,2]
    
    for range in ranges:
        for groupingType in GROUPTYPE:
            for model in models:
                for limit in limits:
                    RadarGraph(groupingType, model, limit, range)

drawRadarGraph()
    




