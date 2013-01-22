'''
Created on 8.1.2013.

@author: Jurica Seva

PhD Candidate 
Faculty of Organization and Informatics
University of Zagreb

Functions:

1. prepareComparisonDocuments(sql, useVectorModel="")
2. documentVScorpus(document)
3. corpusToDOcumentCompare(document)
4.
5.
'''
#imports
import logging, sys, gensim
from gensim import corpora, models, similarities
from python.utils.databaseODP import dbQuery
from python.utils.textPrepareFunctions import removePunct,removeStopWords
from python.utils.createVectorModel import vectorizeDocument

#logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#test data
testSentence = "Split string by the occurrences of pattern. If capturing parentheses are used in pattern, then the text of all groups in the pattern are also returned as part of the resulting list. If maxsplit is nonzero, at most maxsplit splits occur, and the remainder of the string is returned as the final element of the list. (Incompatibility note: in the original Python 1.5 release, maxsplit was ignored. This has been fixed in later releases.)"

#functions     
def prepareComparisonDocuments(sql, useVectorModel=""):
    """
    Input parameters: 
    sql: SQL query (text/variable) where second select parameter has to be desription field in the table that is queried against            
    useVectorModel: which vector space model to use (tfidf default, model file testNewsgroups.tfidf_model)
    
    Output parameters:
    Returned documents from SQL query in specified vector space model (tf-idf by default)
    """
    #SQL processing
    results = dbQuery(sql)
    
    #sql result processing
    data = []    
    for row in results:
        noPunct = ""
        #dataNLTK = nltk.clean_html(row[1])
        #soup = BeautifulSoup(row[1])
        #print "NLTK clean_html ", dataNLTK
        #print "BS4 ",soup.get_text()
        noPunct = removePunct(row[1], 1)
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
        

def documentVScorpus(document):
    """
    List of documents
    create td idf model from saved corpora on disk
    take document and compare to model, loaded from disk
    print document in tf idf model    
    """
    #prepare corpus for transformation
    dictionary = corpora.Dictionary.load('dictionaries/testNewsgroupsDictionary.dict')
    corpus = corpora.MmCorpus('corpusFiles/testNewsgroupsMmCorpus.mm')
    #print dictionary
    #print corpus
    tfidf = models.TfidfModel.load('models/testNewsgroups.tfidf_model')
    #print tfidf
       
    """
    Testing transformation
    doc_bow = [(0, 1), (1, 1),(4,3),(17,9)]
    print tfidf[doc_bow]
    """
    
    #prepare document; remove punctuation, stopWords, return bow format
    processedDoc = vectorizeDocument(document)
    print processedDoc

    #transformation of new document to existing model
    for doc in processedDoc:
        documentTfIDF = tfidf[doc]
        print documentTfIDF, "\n"
        
    #similarity to trained model
    corpus = corpora.MmCorpus('corpusFiles/testNewsgroupsMmCorpus.mm')
    index = similarities.MatrixSimilarity(tfidf[corpus])
    sims = index[documentTfIDF]
    print list(enumerate(sims))
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    print sims

def corpusToDOcumentCompare(document):
    """
    create td idf model from saved corpora on disk
    take document and compare to model, loaded from disk
    print document / model 
    dummy comparison function; not to be used further
    """
    #prepare corpus for transformation
    dictionary = corpora.Dictionary.load('dictionaries/testNewsgroupsDictionary.dict')
    corpus = corpora.MmCorpus('corpusFiles/testNewsgroupsMmCorpus.mm')
   
    #read tfidf model
    tfidf = models.TfidfModel.load('models/testNewsgroups.tfidf_model')
    print tfidf
    
    #Test document
    doc_bow = [(0, 1), (1, 1),(4,3),(7,9)]
    #print tfidf[doc_bow]
    
    #Test document based on tfidf model 
    vec_bow = tfidf[doc_bow]
    #print vec_bow
    
    #similarity
    index = similarities.MatrixSimilarity(tfidf[corpus])
    similarity = index[vec_bow]
    sims = sorted(enumerate(similarity), key=lambda item: -item[1])
    print sims

def main():
    """
    Functions:
        1. prepareComparisonDocuments(sql, useVectorModel="")
        2. corpusToDOcuments(document)
        3. corpusToDOcumentCompare(document)
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
    elif var == "3":
        print prepareComparisonDocuments.__doc__
        var1 = raw_input("Insert SQL query")
        prepareComparisonDocuments(sql=var1)
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        

if __name__ == '__main__':    
    main()