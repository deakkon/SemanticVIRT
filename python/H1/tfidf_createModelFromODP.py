'''
Created on 9.1.2013.

@author: Jurica Seva

PhD Candidate 
Faculty of Organization and Informatics
University of Zagreb

Functions:
    1. createTFIDFfromODP_dmoz_descriptions(topic="",depthStart="", depthEnd="")
    2. createTrainingData()
'''
#imports
import logging, sys
from python.utils.databaseODP import dbQuery, errorMessage
from python.utils.createVectorModel import createCorpusAndVectorModel,getCategoryLabel

#logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#functions
def createTFIDFfromODP_dmoz_descriptions(topic="",depthStart="", depthEnd=""):
    """
    Input paramters:
        1. topic
            Available topics:
            "Title"
            "Arts"
            "Business"
            "Computers"
            "Games"
            "Health"
            "Home"
            "Kids_and_Teens"
            "News"
            "Recreation"
            "Reference"
            "Regional"
            "Science"
            "Shopping"
            "Society"
            "Sports"
        2. depthStart
        3. depthEnd
        
        TESTING PURPOSES
    """
        
    #if any of the arguments emty exit
    if topic == "":
        errorMessage("First paramter is missing")    
    if depthStart == "": 
        errorMessage("Second paramter is missing")    
    if depthEnd == "":
        errorMessage("Third paramter is missing")
    
    #data from db
    sql = "select Description from dmoz_categories where Topic like '%/"+str(topic)+"/%' and categoryDepth >= '"+str(depthStart)+"' and categoryDepth <= '"+str(depthEnd)+"'"
    res = dbQuery(sql)
    
    #create dynamic file names
    saveFileName = str(topic)+"_"+str(depthStart)+"_"+str(depthEnd)    
    #print saveFileCorpus, "    ",saveFileModel
    
    #create corpora and model from db query results
    createCorpusAndVectorModel(res,fileName=saveFileName)

def createTrainingData():
    """
    1. get root categories to be used and iterate through main categories
    3. get max depth for individual category
    4. from 1 to max till 1 to 1
        get all catid for iterated category
        get all pages for selected categories
        call createCorpusAndVectorModel fro selected documents
     
    """
    #get root categories to be used
    sqlMainCategories = "select distinct(Title) from dmoz_categories where dmoz_categories.categoryDepth = 1 and dmoz_categories.filterOut = 0"
    mainCat = dbQuery(sqlMainCategories)
    
    #iterate through main categories
    for cat in mainCat:
        print cat[0]
        sqlmaxDepth = "select max(categoryDepth) from dmoz_categories where Topic like '%/"+str(cat[0])+"/%' and filterOut = 0"
        maxDebthRS = dbQuery(sqlmaxDepth)
        maxDebth = maxDebthRS[0]
        print "cat max depth: ",maxDebth
        #catLabels = []
        
        #dynamic sql for depth levels to be queried, extracting all catid values for category cat between depthLevels 1 and maxDepth, with maxDepth-- each iteration
        while maxDebth != 1:

            #limited to 10 000 pages per Topic per level
            #sqlFromTo = "select Description,Title,link from dmoz_externalpages where catid in (select catid from dmoz_categories where Topic like '%/"+cat[0]+"/%' and categoryDepth >=1 and categoryDepth <= "+str(maxDebth)+" and filterOut = 0)"
            #sqlFromToSame = "select Description,Title,link from dmoz_externalpages where catid in (select catid from dmoz_categories where Topic like '%/"+cat[0]+"/%' and categoryDepth >=1 and categoryDepth <= "+str(maxDebth)+" and filterOut = 0) LIMIT 1000"            
            #sqlLabelsBetween = "select Title, catid from dmoz_categories where Topic like '%/"+cat[0]+"/%' and Description != '' and categoryDepth >=1 and categoryDepth <= "+str(maxDebth)
            #sqlLabelsCategory = "select Title, catid from dmoz_categories where Topic like '%/"+cat[0]+"/%' and categoryDepth = "+str(maxDebth)
            
            #!!!to be run on the virtual machine!!!
            sqlFromTo = "select Description,Title,link from dmoz_externalpages where catid in (select catid from dmoz_categories where Topic like '%/"+cat[0]+"/%' and categoryDepth >=1 and categoryDepth <= "+str(maxDebth)+" and filterOut = 0)"
            sqlFromToSame = "select Description,Title,link from dmoz_externalpages where catid in (select catid from dmoz_categories where Topic like '%/"+cat[0]+"/%' and categoryDepth >=1 and categoryDepth <= "+str(maxDebth)+" and filterOut = 0)"            
            sqlLabelsBetween = "select distinct(Title) from dmoz_categories where Topic like '%/"+cat[0]+"/%' and Description != '' and categoryDepth >=1 and categoryDepth <= "+str(maxDebth)
            sqlLabelsCategory = "select distinct(Title) from dmoz_categories where Topic like '%/"+cat[0]+"/%' and categoryDepth = "+str(maxDebth)
            
            #print "local max depth ", maxDebth
            maxDebth -= 1
            fileName = cat[0]+"_1_"+str(maxDebth)
            fileNameLabelsCategory = cat[0]+"_"+str(maxDebth) 
            
            #prints for debugging
            #print "file name: ",fileName            
            #print sqlFromTo
            #print sqlLabelsBetween|
            #print sqlLabelsCategory
            
            createCorpusAndVectorModel(sqlFromTo, fileName=fileName)
            createCorpusAndVectorModel(sqlFromToSame, fileName=fileName)
            getCategoryLabel(sqlLabelsBetween,fileName)
            getCategoryLabel(sqlLabelsCategory,fileNameLabelsCategory)

def createModelFromAll():
    """
    Created tf idf model from entire database     
    """    
    sqlQuery = "select Description from dmoz_externalpages"
    sqlLabelsBetween = "select Title, catid from dmoz_categories"
    fileName = "allData"
    createCorpusAndVectorModel(sqlQuery, fileName=fileName)
    getCategoryLabel(sqlLabelsBetween,fileName)
           
#main function
def main():
    """
Functions:
    1. createTFIDFfromODP_dmoz_descriptions(topic="",depthStart="", depthEnd="")
    2. createTrainingData()
    3. createModelFromAll():
    """ 
    print main.__doc__

    var = raw_input("Choose function to run: ")
        
    if var == "1":
        print createTFIDFfromODP_dmoz_descriptions.__doc__
        var1 = raw_input("Insert Topic Name to query")
        var2 = raw_input("Start depth for topic ")
        var3 = raw_input("End depth for topic ")
        print createTFIDFfromODP_dmoz_descriptions(var1,var2,var3)
    elif var == "2":
        print createTrainingData.__doc__
        print createTrainingData()
    elif var == "3":
        print createModelFromAll.__doc__
        print createModelFromAll()        
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        
if __name__ == '__main__':    
    main()