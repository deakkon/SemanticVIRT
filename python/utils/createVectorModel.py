'''
Created on 2.1.2013.

@author: Jurica

Functions:
    1.vectorizeDocument(document)
    2.createCorpusAndVectorModel(documents, outputFormat=1, modelFormat=1, fileName ="")


version o.1
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

Version 0.2
    Working with sql queries 
'''
#imports
import logging, sys
from gensim import corpora, models
from python.utils.textPrepareFunctions import removePunct, removeStopWords 
from python.utils.databaseODP import dbQuery, errorMessage


#logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#variables
manualStopWords = []
lisType = []

#test data
#sql = "select dmoz_newsgroups.catid, dmoz_categories.Description as catDesc from dmoz_categories, dmoz_newsgroups where dmoz_categories.catid = dmoz_newsgroups.catid and dmoz_categories.Description != '' group by dmoz_newsgroups.catid limit 100"
#results = dbQuery(sql)
#sentence = "Split string by the occurrences of pattern. If capturing parentheses are used in pattern, then the text of all groups in the pattern are also returned as part of the resulting list. If maxsplit is nonzero, at most maxsplit splits occur, and the remainder of the string is returned as the final element of the list. (Incompatibility note: in the original Python 1.5 release, maxsplit was ignored. This has been fixed in later releases.)"


#functions
def vectorizeDocument(document):
    """
    Input: single document
    Output: BoW representation of a single document, tpye python list
    Doesn't save the dictionary 
    """   
    #document preparation: remove puncuation and stopwords
    #print "Starting text: ", document
    #print "length 1", len(document)
    document = [removeStopWords(removePunct(document, 1))]
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

def createCorpusAndVectorModel(sqlQuery="", outputFormat=1, modelFormat=1, fileName =""):
    """
    Input parameters: sqlQueryResults="", outputFormat=1, modelFormat=1, fileName =""
        1. sqlQueryResults -> if "" use dummy data, textual column to be analyzed first parameter in query
        2. outputFormat definition:     1 -> MmCorpus (default)
                                        2 -> SvmLightCorpus
                                        3 -> BleiCorpus
                                        4 -> LowCorpus
        3. modelFormat:                 1 -> tfidf_model (default)
                                        2 -> lsi
                                        3 -> lda
        4. fileName -> if "" use dummy name
                                                                                                                
            
    Output data: saved dictionary, corpus and model files of chosen format to disk, to respected directories
    """
    #variables
    data = []
    
    #create file names to save
    if fileName == "":
        fileName = "defaultCollection"
    
    #type
    print type(sqlQuery)
    
    #default data
    if sqlQuery == "":
        sqlQuery = "select Description from dmoz_categories where Description != '' limit 1000"
        sqlQueryResults = dbQuery(sqlQuery)
    elif type(sqlQuery) is str:
        sqlQueryResults = dbQuery(sqlQuery)
    elif type(sqlQuery)is tuple:
        sqlQueryResults = sqlQuery
    else:
        print type(sqlQuery)
        print "yaba daba doo createVectorModel createCorpusAndVectorModel "
        sys.exit(1)
         
    
    #iteration rhrough supplied documents
    for row in sqlQueryResults:
        noPunct = ""
        #dataNLTK = nltk.clean_html(row[1])
        #soup = BeautifulSoup(row[1])
        #print "NLTK clean_html ", dataNLTK
        #print "BS4 ",soup.get_text()
        noPunct = removePunct(row[0], 1)
        data.append(removeStopWords(noPunct))
            
    #print "Stop words ",data
    print data
    dictionary = corpora.Dictionary(data)
    #print dictionary.token2id
        
    #creating dictionary and corpus  files in different matrix formats    
    bow_documents = [dictionary.doc2bow(text) for text in data]
    dictFN = "dictionaries/"+fileName+".dict"
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
        
def main():
    """
    Functions:
        1.vectorizeDocument(document)
        2.createCorpusAndVectorModel(documents, outputFormat=1, modelFormat=1, fileName ="")
    """ 
    print main.__doc__

    var = raw_input("Choose function to run: ")
        
    if var == "1":
        print vectorizeDocument.__doc__
        var1 = "Input text to vectorize"
        print vectorizeDocument(var1)
    elif var == "2":
        print createCorpusAndVectorModel.__doc__
        print "No input parameters needed. Works with dummy data to show functionality."
        createCorpusAndVectorModel()        
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        
if __name__ == '__main__':    
    main()