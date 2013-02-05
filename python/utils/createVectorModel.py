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
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#imports
import logging, sys, csv, os, string
from gensim import corpora, models
from python.utils.textPrepareFunctions import removePunct, removeStopWords 
from python.utils.databaseODP import dbQuery, errorMessage


#logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#variables
manualStopWords = []
lisType = []

#functions
def vectorizeDocument(document):
    """
    Input: single document
    Output: BoW representation of a single document, tpye python list
    Doesn't save the dictionary 
    
    NOT USED
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
    return bow_document

def createCorpusAndVectorModel(sqlQuery="", outputFormat=1, modelFormat=1, fileName =""):
    """
    Input parameters: sqlQueryResults="", outputFormat=1, modelFormat=1, fileName =""
        1. sqlQueryResults -> if "" exit, textual column to be analyzed first parameter in query
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
    
    #type TEST PRINT
    #print type(sqlQuery)
    
    #default data
    if sqlQuery == "":
        sys.exit("No query mate. Function createCorpusAndVectorModel")
    elif type(sqlQuery) is str:
        sqlQueryResults = dbQuery(sqlQuery)
    elif type(sqlQuery) is tuple:
        sqlQueryResults = sqlQuery
    else:
        print type(sqlQuery)
        print "ERROR createVectorModel createCorpusAndVectorModel "
        sys.exit(1)
         
    
    #iteration through supplied documents
    for row in sqlQueryResults:
        #noPunct = ""
        #dataNLTK = nltk.clean_html(row[1])
        #soup = BeautifulSoup(row[1])
        #print "NLTK clean_html ", dataNLTK
        #print "BS4 ",soup.get_text()
        #noPunct = removePunct(row[0],1)
        data.append(removeStopWords(row[0]))
            
    #print "Stop words ",data
    #print data
    #create dictionary
    dictionary = corpora.Dictionary(data)
    dictFN = "dictionaries/"+fileName+".dict"
    dictionary.save(dictFN)
    #print dictionary.token2id
        
    #creating dictionary and corpus  files in different matrix formats    
    bow_documents = [dictionary.doc2bow(text) for text in data]

    #create corpora data for use in creating a vector model representation for furher use
    if outputFormat == 1:
        saveFN = "corpusFiles/"+fileName+".mm"
        corpora.MmCorpus.serialize(saveFN, bow_documents)
    elif outputFormat == 2:
        saveFN = "corpusFiles/"+fileName+".svmlight"
        corpora.SvmLightCorpus.serialize(saveFN, bow_documents)
    elif outputFormat == 3:
        saveFN = "corpusFiles/"+fileName+".lda-c"
        corpora.BleiCorpus.serialize(saveFN, bow_documents)
    elif outputFormat == 4:
        corpora.LowCorpus.serialize(saveFN, bow_documents)
        saveFN = "corpusFiles/"+fileName+".low" 
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
        
def getCategoryLabel(sqlQuery,fileName):
    """
    sqlQuery -> query to be executed or query result set
    fileName -> file to save labels returned by the query
    """
    #variables
    categoryLabels = []
    
    #default data
    if sqlQuery == "":
        sys.exit("No query mate. Function getCategoryLabel")
    elif type(sqlQuery) is str:
        sqlQueryResults = dbQuery(sqlQuery)
    elif type(sqlQuery) is tuple:
        sqlQueryResults = sqlQuery
    else:
        print type(sqlQuery)
        print "error createVectorModel getCategoryLabel "
        sys.exit(1)
    
    #print executed query
    #print sqlQuery
        
    #iteration through documents   
    for row in sqlQueryResults:
        if type(row) is not long:
            #print type(row)," :: ",type(row[0]), row[0]
            #missing: remove stop words, punctuation, names
            categoryLabels.append(removeStopWords(row[0]))   
            #categoryLabels.append(str(row[0]))
        
    #print sqlQueryResults
    #categoryLabels = [row[0] for row in sqlQueryResults]
    #print categoryLabels
    """
    dictionary = corpora.Dictionary(categoryLabels)
    dictFN = "labels/"+fileName+".dict"
    dictionary.save(dictFN)
    """

    #path to save the file    
    if os.path.realpath(__file__)== "/home/jseva/SemanticVIRT/python/utils/createVectorModel.py":
        fileName = "../H1/labels/"+fileName+".csv"
    else:
        fileName = "labels/"+fileName+".csv"    
    
    out = csv.writer(open(fileName,"w"), delimiter=',',quoting=csv.QUOTE_ALL)
    
    writeLabels = []
    #append to file
    print string.letters
    for row in categoryLabels:
        print row
        #print type(row)
        #print len(row)
        for i in row:            
            if i != "" or i.lower() not in string.letters.lower():
                #print i.lower()
                #out.writerow(i)
                writeLabels.append(i.lower())
    print writeLabels
    out.writerow(writeLabels)
    #return categoryLabels 

        
def returnFatherIDs(sqlQuery):
    """
    Group catid, on specific depth level,  based on their fatherID values
    sql query -> fatherID first level 
    Returns fatherID on level x    
    """
    #variables
    fatherIDLevel = []
    
    if sqlQuery == "":
        sys.exit("No query mate. Function getCategoryLabel")
    elif type(sqlQuery) is str:
        sqlQueryResults = dbQuery(sqlQuery)
    elif type(sqlQuery) is tuple:
        sqlQueryResults = sqlQuery
    else:
        print type(sqlQuery)
        print "yaba daba doo createVectorModel getCategoryLabel "
        sys.exit(1)
        
    #iterate through returned
    for row in sqlQueryResults:
        #print row[0]
        fatherIDLevel.append(row[0])
        
    #return values 
    return fatherIDLevel

def main():
    """
    Functions:
        1.vectorizeDocument(document)
        2.createCorpusAndVectorModel(documents, outputFormat=1, modelFormat=1, fileName ="")
        3.getCategoryLabel(sqlQuery,fileName)
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
    elif var == "3":
        print getCategoryLabel.__doc__
        var1 = raw_input("Input SQl query")
        var2 = raw_input("fileName for the file to be created")
        print getCategoryLabel(var1,var2)           
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        
if __name__ == '__main__':    
    main()