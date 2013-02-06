'''
Created on 8.1.2013.

@author: Jurica Seva

PhD Candidate 
Faculty of Organization and Informatics
University of Zagreb

Functions:

1. prepareComparisonDocuments(sql, useVectorModel="")
2. documentVScorpus(document)
'''
#imports
import logging, sys, os, glob
from gensim import corpora, models, similarities
from python.utils.databaseODP import dbQuery
from python.utils.textPrepareFunctions import removeStopWords

#logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#functions     
def prepareComparisonDocuments(sqlQuery):
    """
    Input: 
        sqlQuery to be executed, first parameter being textual data to convert to BoW
        
    Output parameters:
        BoW representation of documents returned from sqlQuery, list of lists
    """
    #check sqlQuery
    if sqlQuery == "":
        sys.exit("No query mate. Function prepareComparisonDocuments")
    elif type(sqlQuery) is str:
        sqlQueryResults = dbQuery(sqlQuery)
    elif type(sqlQuery) is tuple:
        sqlQueryResults = sqlQuery
    else:
        print type(sqlQuery)
        print "yaba daba doo calculateSimilarity.prepareComparisonDocuments() "
        sys.exit(1)    
    
    #get data from DB
    sqlQueryResults = dbQuery(sqlQuery)
    
    #variabless
    bowTemp = []
    bowReturn = []
    dictionary = corpora.Dictionary()
        
    #prepare BoW
    for row in sqlQueryResults:
        bowTemp = removeStopWords(row[0])
        bowTemp = [dictionary.doc2bow(text) for text in bowTemp]
        bowReturn.extend(bowTemp)            
    
    return bowReturn

#get model files from folder
def getFileList(folder):
    """
    List test model files in folder, with folder being 1000 or 5000
    Input: folder \n -> 1 = 1000 \n 2 -> 5000 \n 3 -> all data            
    """
    if folder == "1":
        path = "testData/1000/models/*.tfidf*"
    elif folder == "2":
        path = "testData/5000/models/*.tfidf*"
    elif folder == "3":
         path = "fullDataPP/models/*.tfidf*"
    else:
        sys.exit("Wrong choice. calculateSimilarity.getFileList()")  
    
    #print glob.glob(path)
    return glob.glob(path)
        
def returnSimilarities():
    """
    Input: 
        bowDocument -> BoW representation of document for similarity comparison
    
    Output:
        list of top n similar documents from tfidf model
    """
    #variables
    modelList = []
    depthDescirption = []
    
    #get random category
    sqlMainCategories = "select distinct(Title) from dmoz_categories where dmoz_categories.categoryDepth = 1 and dmoz_categories.filterOut = 0 and filterOut = 0 order by rand() limit 1"
    print sqlMainCategories
    mainCat = dbQuery(sqlMainCategories)
    randomCat = mainCat[0]
    print randomCat
    
    #get cat debth
    sqlCatDebth = "select max(categoryDepth) from dmoz_categories where Topic like '%/"+str(randomCat)+"/%'"
    print sqlCatDebth
    catDepthRow = dbQuery(sqlCatDebth)
    catDepth = catDepthRow[0]
    print catDepth
    
    #get random documents from database for cat; get catid and all files from dmoz_externalpages for each catid
    for depth in range(2,catDepth):    
        sqlRandom = "SELECT ep.Description, ep.catid FROM dmoz_externalpages ep LEFT JOIN dmoz_categories c ON ep.catid = c.catid where Topic like '%/"+str(randomCat)+"/%' and categoryDepth = "+str(depth)+" ORDER BY rand() LIMIT 1000"
        prepareComparisonDocuments(sqlRandom)
        print sqlRandom
        descriptionRow = dbQuery(sqlRandom)
        print type(descriptionRow)
        depthDescirption.append(descriptionRow)
        
    #print depthDescirption        
    
    """
    #choose comparison model
    print "Choose model for comparison: 1 = 1000 \n 2 -> 5000 \n 3 -> all data"
    chosenModel = raw_input(": ")
    modelList = getFileList(chosenModel)
    
    #load model
    tfidf = models.TfidfModel.load(tfidfFN)

    #for each dowcument in bow representation
    for doc in bowDocument:
        documentTfIDF = tfidf[doc]
        #print documentTfIDF, "\n"
        
        #load corpus for similarity index
        
        
        #similarity to trained model
        index = similarities.MatrixSimilarity(tfidf)
        sims = index[documentTfIDF]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        print sims
    """

def main():
    """
    Functions:
        1. prepareComparisonDocuments(sqlQuery)
        2. getFileList(folder)
        3. returnSimilarities()
        Anything else to stop
     """
    print main.__doc__

    var = raw_input("Enter something: ")
        
    if var == "1":
        print prepareComparisonDocuments.__doc__
        var1 = raw_input("Insert SQL query")
        prepareComparisonDocuments(var1)        
    elif var == "2":
        print getFileList.__doc__
        var1 = raw_input("Choose test data version: ")
        getFileList(var1)
    elif var == "3":
        print returnSimilarities.__doc__
        returnSimilarities()
        
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        

if __name__ == '__main__':    
    main()