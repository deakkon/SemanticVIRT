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
import logging, sys
from gensim import corpora, models, similarities
from python.utils.databaseODP import dbQuery
from python.utils.textPrepareFunctions import removePunct,removeStopWords
from python.utils.createVectorModel import vectorizeDocument

#logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#test data
testSentence = "Split string by the occurrences of pattern. If capturing parentheses are used in pattern, then the text of all groups in the pattern are also returned as part of the resulting list. If maxsplit is nonzero, at most maxsplit splits occur, and the remainder of the string is returned as the final element of the list. (Incompatibility note: in the original Python 1.5 release, maxsplit was ignored. This has been fixed in later releases.)"

#functions     
def prepareComparisonDocuments(sqlQuery, useVectorModel=""):
    """
    Input parameters: 
    sql: textual column to be analyzed first parameter in query       
    useVectorModel: which vector space model to use (tfidf default, model file testNewsgroups.tfidf_model)
    
    Output parameters:
    Returned documents from SQL query in specified vector space model (tf-idf by default)
    """
    #default data
    if sqlQuery == "":
        sys.exit("No query mate. Function getCategoryLabel")
    elif type(sqlQuery) is str:
        sqlQueryResults = dbQuery(sqlQuery)
    elif type(sqlQuery) is tuple:
        sqlQueryResults = sqlQuery
    else:
        print type(sqlQuery)
        print "yaba daba doo createVectorModel createCorpusAndVectorModel "
        sys.exit(1)    
    
    #sql result processing
    data = []    
    for row in sqlQueryResults:
        noPunct = ""
        #dataNLTK = nltk.clean_html(row[1])
        #soup = BeautifulSoup(row[1])
        #print "NLTK clean_html ", dataNLTK
        #print "BS4 ",soup.get_text()
        noPunct = removePunct(row[0], 1)
        data.append(removeStopWords(noPunct))
    
    #create dict and bow format
    dictionary = corpora.Dictionary(data)
    bow_documents = [dictionary.doc2bow(text) for text in data]
    
    #load model specified with useVectorModel
    tfIdfModel = models.TfidfModel.load('models/testNewsgroups.tfidf_model')
    #print tfIdfModel
    
    #convert prepared documents to TfDdf space, based on saved model, and return the results
    vec_tfidf = tfIdfModel[bow_documents]
    #print vec_tfidf
    return vec_tfidf
        
def documentVScorpus(document,comparisonModel=""):
    """
    List of documents
    create td idf model from saved corpora on disk
    take document and compare to model, loaded from disk
    print document in tf idf model    
    """
    
    #inital input variable check
    if comparisonModel == "":
        comparisonModel = "testNewsgroups"
    
    #dict, corpus, tfidf model filenames
    dcitionaryFN = "dictionaries/"+str(comparisonModel)+"Dictionary.dict"
    corpusFN = "corpusFiles/"+str(comparisonModel)+".mm"
    tfidfFN = "models/"+str(comparisonModel)+".tfidf_model"
    
    #prepare corpus for transformation
    dictionary = corpora.Dictionary.load(dcitionaryFN)
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
        3. 
        Anything else to stop
     """
    print main.__doc__

    var = raw_input("Enter something: ")
        
    if var == "1":
        print prepareComparisonDocuments.__doc__
        var1 = raw_input("Insert SQL query")
        prepareComparisonDocuments(sql=var1)        
    elif var == "2":
        print documentVScorpus.__doc__
        var1 = raw_input("Insert document: ")
        documentVScorpus(var1)
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        

if __name__ == '__main__':    
    main()