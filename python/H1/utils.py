import sys, csv
from sys import path
path.append("/home/jseva/SemanticVIRT/python/utils/")
from databaseODP import *

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

def getCSV_Colmn(file,column):
    returnValues = []
    rownum = 0
    mycsv = csv.reader(open(file))
    for row in mycsv:
        if rownum == 0:
            header = row
            #print row
        else:        
            returnValues.append(row[column])
        rownum += 1
    
    return returnValues

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
    name = "testData_classificationModels/%s/%s.png" %(model,name)
    plt.savefig(name)

def computeClassificationMetrics(y_true,y_pred):
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    F1 = f1_score(y_true, y_pred)
    return (precision,recall, F1)

def returnDirectoryList(path):
    directories = []
    
    for files in os.listdir(path): 
        if os.path.isdir(os.path.join(path,files)):
            #print "Directory : ",files
            directories.append(files)
    return directories
