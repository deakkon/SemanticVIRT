'''
Created on 2.1.2013.

@author: Jurica Seva

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

#imports0
import logging, sys, csv, os, string
import gensim
from gensim import corpora, models
#from python.utils.textPrepareFunctions import removePunct, removeStopWords 
#from python.utils.databaseODP import dbQuery, errorMessage
from ShevaDB import ShevaDB
#from ShevaTPF import ShevaTPF


class ShevaVect:
    """
    def __init__(self):
        #logging
        #logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        self.manualStopWords = []
        self.listType = []
    """
    #functions
    def vectorizeDocument(self, data):
        """
        1. document -> prepared data for data creation
        """
        #create dictionary
        dictionary = gensim.corpora.Dictionary(data)
        dictFN = "%sdict/%s.dict" %(path,fileName)
        dictionary.save(dictFN)        
        dictionary = corpora.Dictionary(document)
        bow_document = [dictionary.doc2bow(text) for text in document]
        return bow_document
    
    def createCorpus(self,path,fileName,data,outputFormat):
       #create corpora data for use in creating a vector model representation for furher use
        corpora = "%scorpus/%s"%(path,fileName)
        if outputFormat == 1:
            saveCorpora = "%s.mm"%(corpora)
            gensim.corpora.MmCorpus.serialize(saveCorpora, data)
        elif outputFormat == 2:
            saveCorpora = "%s.svmlight"%(corpora)
            gensim.corpora.SvmLightCorpus.serialize(saveCorpora, data)
        elif outputFormat == 3:
            saveCorpora = "%s.lda-c" %(corpora)
            gensim.corpora.BleiCorpus.serialize(saveCorpora, data)
        elif outputFormat == 4:
            saveCorpora = "%s.low"%(corpora) 
            gensim.corpora.LowCorpus.serialize(saveCorpora, data)
        else:
            errorMessage("Unknown corpus type identificator")

    
    def createModel(self,path,fileName,data,modelFormat):
        #save model to disk -> model of all documents that are going to be compared against
        model = "%smodels/%s"%(path,fileName)
        if modelFormat == 1:
            tfidf = gensim.models.TfidfModel(data)
            saveModel = "%s.tfidf_model"%(model)
            tfidf.save(saveModel)
        elif modelFormat == 2:
            lsi = gensim.models.LsiModel(data)
            saveModel = "%s.lsi" %(model)
            lsi.save(saveModel)
        elif modelFormat == 3:
            lda = gensim.models.LdaModel(data)
            saveModel = "%s.lda"%(model)
            lda.save(saveModel)
        else:
            errorMessage("createTrainingModel: Something went wrong with the type identificator")
    
    def createCorpusAndVectorModel(self,data, fileName, path, outputFormat=1, modelFormat=1):
        """
        Input parameters: sqlQueryResults="", outputFormat=1, modelFormat=1, fileName =""
            1. data     -> prepared data (removed all stopwrods etc) to save to models, corpus, dictionary type list of lists
                           each document list element of data list                            
            3. fileName -> name to save file, dynamically assigned by caller function (E.G. 0.1_arts_6)
            3. path     ->  location to save dictionary, corpus and model files
            4. outputFormat definition:     1 -> MmCorpus (default)
                                            2 -> SvmLightCorpus
                                            3 -> BleiCorpus
                                            4 -> LowCorpus
            5. modelFormat:                 1 -> tfidf_model (default)
                                            2 -> lsi
                                            3 -> lda                                                                                                                            
        Output data: saved dictionary, corpus and model files of chosen format to disk, to respected directories
        """

        #create dictionary
        dictionary = gensim.corpora.Dictionary(data)
        dictFN = "%sdict/%s.dict" %(path,fileName)
        dictionary.save(dictFN)

        #creating dictionary and corpus  files in different matrix formats    
        bow_documents = [dictionary.doc2bow(text) for text in data]

        self.createCorpus(path,fileName, bow_documents, outputFormat)
        self.createModel(path,fileName, bow_documents, modelFormat)

    def getCategoryLabel(self,sqlQuery,fileName):
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
            sqlQueryResults = ShevaDB().dbQuery(sqlQuery)
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
    
            
    def returnFatherIDs(self,sqlQuery):
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
            sqlQueryResults = ShevaDB().dbQuery(sqlQuery)
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