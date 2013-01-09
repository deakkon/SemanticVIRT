'''
Created on 8.1.2013.

@author: Jurica Seva

PhD Candidate 
Faculty of Organization and Informatics
University of Zagreb
'''
#imports
import logging
from gensim import models, corpora, similarities
from python.ODP_analysis.utils import *
from python.ODP_analysis.H1.createModel import *

#logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#test data
testSentence = "Split string by the occurrences of pattern. If capturing parentheses are used in pattern, then the text of all groups in the pattern are also returned as part of the resulting list. If maxsplit is nonzero, at most maxsplit splits occur, and the remainder of the string is returned as the final element of the list. (Incompatibility note: in the original Python 1.5 release, maxsplit was ignored. This has been fixed in later releases.)"

#functions     
def prepareComparisonDocuments(sql):
    """
    Takes in set of documents and prepares them for similarity calculations
    Uses TF IDF model created by createTrainingModel()
    
    Input parameters: sql query
    Output parameters: processed set of documents, represented through saved tfidf model (currently, testing corpus from newsgroup db table 
    The results are input to similarity calculations
    """
    con = dbConnect()
    results = dbQuery(con, sql)
    
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
    
    tfIdfModel = models.TfidfModel.load('models/testNewsgroups.tfidf_model')
    #print tfIdfModel
    
    #convert prepared documents to TfDdf space, based on saved model, and return the results
    vec_tfidf = tfIdfModel[bow_documents]
    #print vec_tfidf
    return vec_tfidf
        

def corpusToDOcuments(document):
    """
    List of documents
    create td idf model from saved corpora on disk
    take document and compare to model, loaded from disk
    print document in tf idf model
    """
    #prepare corpus for transformation
    dictionary = corpora.Dictionary.load('corpusFiles/testNewsgroupsDictionary.dict')
    corpus = corpora.MmCorpus('corpusFiles/testNewsgroupsMmCorpus.mm')
    #print dictionary
    #print corpus
    tfidf = models.TfidfModel.load('models/testNewsgroups.tfidf_model')
    print tfidf
       
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

def corpusToDOcumentCompare(document):
    """
    create td idf model from saved corpora on disk
    take document and compare to model, loaded from disk
    print document / model 
    dummy comparison function; not to be used further
    """
    #prepare corpus for transformation
    dictionary = corpora.Dictionary.load('corpusFiles/testNewsgroupsDictionary.dict')
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
    
    
#corpusToDOcumentCompare()
#corpusToDOcuments(testSentence)