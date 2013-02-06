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
        bowTemp = [dictionary.doc2bow(text) for text in bow_documents]
        bowReturn.extend(bowTemp)            
    
    return bowReturn

#get model files from folder
def getFileList(folder):
    """
    List test model files in folder, with folder being 1000 or 5000
    
    Input: folder -> 1 = 1000 \n 2 -> 5000
            
    """
    if folder == "1":
        path = "testData/1000/models/*.tfidf*"
    elif folder == "2":
        path = "testData/5000/models/*.tfidf*"
    else:
        sys.exit("Wrong choice. calculateSimilarity.getFileList()")  
    
    print glob.glob(path)
    return glob.glob(path)
        
def documentVScorpus(bowDocument):
    """
    Input: 
        bowDocument -> BoW representation of document for similarity comparison
    
    Output:
        list of top n similar documents from tfidf model
    """
    
    #dict, corpus, tfidf model filenames
    dictionaryFN = "dictionaries/"+str(comparisonModel)+"Dictionary.dict"
    corpusFN = "corpusFiles/"+str(comparisonModel)+".mm"
    tfidfFN = "models/"+str(comparisonModel)+".tfidf_model"
    
    #prepare corpus for transformation
    #dictionary = corpora.Dictionary.load(dcitionaryFN)
    corpus = corpora.MmCorpus(corpusFN)
    tfidf = models.TfidfModel.load(tfidfFN)
    
    #prepare document; remove punctuation, stopWords, return bow format
    processedDoc = vectorizeDocument(document)


    #transformation of new document to existing model
    for doc in processedDoc:
        documentTfIDF = tfidf[doc]
        print documentTfIDF, "\n"
        
    #similarity to trained model
    index = similarities.MatrixSimilarity(tfidf[corpus])
    sims = index[documentTfIDF]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    print sims

def main():
    """
    Functions:
        1. prepareComparisonDocuments(sql, useVectorModel="")
        2. documentVScorpus(document)
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
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        

if __name__ == '__main__':    
    main()