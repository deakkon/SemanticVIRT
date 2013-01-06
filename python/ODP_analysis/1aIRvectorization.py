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
import nltk
from bs4 import BeautifulSoup
from lxml import html
#user defined functions
from indexingModel import *
from odpDatabase import *


#logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#variables
manualStopWords = []

#test data
sql = "select dmoz_newsgroups.catid, dmoz_categories.Description as catDesc from dmoz_categories, dmoz_newsgroups where dmoz_categories.catid = dmoz_newsgroups.catid and dmoz_categories.Description != '' group by dmoz_newsgroups.catid limit 100"
con = dbConnect()
results = dbQuery(con, sql)

sentence = "Split string by the occurrences of pattern. If capturing parentheses are used in pattern, then the text of all groups in the pattern are also returned as part of the resulting list. If maxsplit is nonzero, at most maxsplit splits occur, and the remainder of the string is returned as the final element of the list. (Incompatibility note: in the original Python 1.5 release, maxsplit was ignored. This has been fixed in later releases.)"


#functions
def vectorizeDocument(document):
    """
    Returns vectorized document 
    """   
    #document preparation: remove puncuation and stopwords
    #print "Starting text: ", document
    #print "length 1", len(document)
    document = removePunct(document, 1)
    document = [removeStopWords(document)]
    #print "length 2", len(document)
    #print "Prepared text: ", len(document),"    ", document, 
    dictionary = corpora.Dictionary(document)
    #print dictionary.token2id
    
    #creating different corpus formats
    corpus = [dictionary.doc2bow(text) for text in document]
    dictionary.save('tmp/test.dict') # store the dictionary, for future reference
    corpora.MmCorpus.serialize('tmp/test.mm', corpus) # store to disk, for later use
    corpora.SvmLightCorpus.serialize('tmp/test.svmlight', corpus)
    corpora.BleiCorpus.serialize('tmp/test.lda-c', corpus)
    corpora.LowCorpus.serialize('tmp/test.low', corpus)
    print corpus
    
    #reading corpuses from file
    corpus1 = corpora.SvmLightCorpus('tmp/test.svmlight')
    print corpus1
    print list(corpus1)

def vectorizeMultiple(documents):
    """
    Takes in documents/SQL results and prepares them for similarity operations
    """
    data = []
        
    for row in documents:
        noPunct = ""
        #dataNLTK = nltk.clean_html(row[1])
        #soup = BeautifulSoup(row[1])
        #print "NLTK clean_html ", dataNLTK
        #print "BS4 ",soup.get_text()
        noPunct = removePunct(row[1], 1)
        data.append(removeStopWords(noPunct))
            
    print "Stop words ",data
    dictionary = corpora.Dictionary(data)
    print dictionary.token2id
        
    #creating different corpus formats    
    corpus = [dictionary.doc2bow(text) for text in data]
    dictionary.save('tmp/test.dict') # store the dictionary, for future reference
    corpora.MmCorpus.serialize('tmp/test.mm', corpus) # store to disk, for later use
    #corpora.SvmLightCorpus.serialize('tmp/test.svmlight', corpus)
    #corpora.BleiCorpus.serialize('tmp/test.lda-c', corpus)
    #corpora.LowCorpus.serialize('tmp/test.low', corpus)
    print corpus        
    
def calculateSimilartiy():
    pass

#vectorizeDocument(sentence)
vectorizeMultiple(results)