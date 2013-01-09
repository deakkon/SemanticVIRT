'''
Created on 2.1.2013.

@author: Jurica

Implementing Gensim Python modules for IR implementation, tested on newsletter corpus:

1. get all documents from a SQL query (depth sensitive)
2: Iterate over documents and perform tokenization/stemming
    2.0 stoplist word removal
    2.1 tokenization: build stop list of words that appear only once
    2.2 tokenization: build stop list of interpunction signs
    2.3 get tokenized text
    2.4 optional -> stem tokenized text (using WN, Porter or Lancaster)
3. bag-of-words representation of documents (each dox one vector)
    3.1 create custom, prepared corpora

'''
#imports
import logging
from gensim import corpora, models, similarities, utils
from gensim.corpora.dictionary import Dictionary
#import nltk
#from bs4 import BeautifulSoup
#from lxml import html
#user defined functions
from indexingModel import *
from python.ODP_analysis.utils.odpDatabase import *


#logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#variables
manualStopWords = []

#test data
sql = "select dmoz_newsgroups.catid, dmoz_categories.Description as catDesc from dmoz_categories, dmoz_newsgroups where dmoz_categories.catid = dmoz_newsgroups.catid and dmoz_categories.Description != '' group by dmoz_newsgroups.catid limit 100"
con = dbConnect()
results = dbQuery(con, sql)

sentence = "Split string by the occurrences of pattern. If capturing parentheses are used in pattern, then the text of all groups in the pattern are also returned as part of the resulting list. If maxsplit is nonzero, at most maxsplit splits occur, and the remainder of the string is returned as the final element of the list. (Incompatibility note: in the original Python 1.5 release, maxsplit was ignored. This has been fixed in later releases.)"

lisType = []

#functions
def vectorizeDocument(document):
    """
    Returns BoW representation of one or more documents 
    """   
    #document preparation: remove puncuation and stopwords
    #print "Starting text: ", document
    #print "length 1", len(document)
    document = removePunct(document, 1)
    document = [removeStopWords(document)]
    #print "length 2", len(document)
    #print "Prepared text: ", len(document),"    ", document, 
    dictionary = corpora.Dictionary(document)
    #print "vectorizeDocument ",dictionary.token2id
    
    #creating different corpus formats
    bow_document = [dictionary.doc2bow(text) for text in document]
    """
    dictionary.save('tmp/test.dict') # store the dictionary, for future reference
    corpora.MmCorpus.serialize('tmp/test.mm', corpus) # store to disk, for later use
    corpora.SvmLightCorpus.serialize('tmp/test.svmlight', corpus)
    corpora.BleiCorpus.serialize('tmp/test.lda-c', corpus)
    corpora.LowCorpus.serialize('tmp/test.low', corpus)
    """
    return bow_document

def createTrainingModel(documents, outputFormat=1, modelFormat=1, fileName =""):
    """
    Take SQL results
    Tag/stem each document
    Add to dictionary
    Create corpus
    Save corpus to file for further use in all gensim supported formats -> outputFormat
    Save model to file for further use in all gensim supported formats -> modelFormat
    """
    #variables
    data = []
    
    #create file names to save
    if fileName == "":
        fileName = "testNewsgroups"
    
    
    #iteration rhrough supplied documents
    for row in documents:
        noPunct = ""
        #dataNLTK = nltk.clean_html(row[1])
        #soup = BeautifulSoup(row[1])
        #print "NLTK clean_html ", dataNLTK
        #print "BS4 ",soup.get_text()
        noPunct = removePunct(row[1], 1)
        data.append(removeStopWords(noPunct))
            
    #print "Stop words ",data
    dictionary = corpora.Dictionary(data)
    #print dictionary.token2id
        
    #creating dictionary and corpus  files in different matrix formats    
    bow_documents = [dictionary.doc2bow(text) for text in data]
    dictFN = fileName+"Dictionary.dict"
    dictionary.save(dictFN)

    #create corpora data for use in creating a vector model representation for furher use
    if outputFormat == 1:
        saveFN = "corpusFiles/"+fileName+"MmCorpus.mm"
        corpora.MmCorpus.serialize(saveFN, bow_documents)
    elif outputFormat == 2:
        saveFN = "corpusFiles/"+fileName+"SvmLightCorpus.svmlight"
        corpora.SvmLightCorpus.serialize(saveFN, bow_documents)
    elif outputFormat == 3:
        saveFN = "corpusFiles/"+fileName+"BleiCorpus.lda-c"
        corpora.BleiCorpus.serialize(saveFN, bow_documents)
    elif outputFormat == 4:
        corpora.LowCorpus.serialize(saveFN, bow_documents)
        saveFN = "corpusFiles/"+fileName+"LowCorpus.low"
    else:
        errorMessage("Something went wrong with the type identificator")
    
    #save model to disk -> model of all documents that are going to be compared against
    if modelFormat == 1:
        tfidf = models.TfidfModel(bow_documents)
        saveFN = "models/"+fileName+".tfidf_model"
        tfidf.save(saveFN)
    elif modelFormat == 2:
        #lsi
        lsi = models.LsiModel(bow_documents)
        saveFN = "models/"+fileName+".lsi"
        lsi.save(saveFN)
    elif modelFormat == 3:
        #lsi
        lda = models.LdaModel(bow_documents)
        saveFN = "models/"+fileName+".lda"
        lda.save(saveFN)
    else:
        errorMessage("createTrainingModel: Something went wrong with the type identificator")
    
 
def documentToBoW(document):
    """
    Takes in string type or tuple type
    If stringType
        convert to list for futher processing 
    If tupe
        continue to processing
        
    NOT IMPLEMENTABLE IN THIS FASHION; STAGE 2
    """
    #input datas
    data = []
    #output data
    dataFinal=[]
    
    if type(document) is str:
        #print 'a string ',type(document)
        #data.append(document.split())
        data.insert(1, document)
        #print data
    elif type(document) is tuple:
        #print 'a tuple',type(document)
        data = document
        #print data
        
    for row in data:
        noPunct = ""
        #print row
        #dataNLTK = nltk.clean_html(row[1])
        #soup = BeautifulSoup(row[1])
        #print "NLTK clean_html ", dataNLTK
        #print "BS4 ",soup.get_text()
        noPunct = removePunct(row[1], 1)
        dataFinal.append(removeStopWords(noPunct))    
    
    #print dataFinal
    dictionary = corpora.Dictionary(dataFinal)
    #print dictionary.token2id
        
    #creating dictionary and corpus  files in different matrix formats    
    bow_documents = [dictionary.doc2bow(text) for text in dataFinal]
    #dictionary.save('corpusFiles/testNewsgroupsDictionary.dict')
    return bow_documents            
        

#print documentToBoW(sentence) -> not working properly, not needed
#vectorizeDocument(sentence)
#createTrainingModel(results,modelFormat=3)
#corpusToDOcumentCompare(sentence)
