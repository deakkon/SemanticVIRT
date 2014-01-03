#imports
import sys

#USER DEFINED MODULES
#sys.path.append("/home/jseva/SemanticVIRT/_utils/")
#from ShevaTPF import ShevaTPF
#from ShevaUtils import ShevaUtils
#from ShevaVect import ShevaVect

#SYS IMPORTS
import gensim
import csv
import random
import os
import numpy

class ShevaSimilarity:
    
    def __init__(self):
        #self.shevaTPF = ShevaTPF()
        #self.shevaUtils = ShevaUtils()
        #self.shevaVect = ShevaVect()
        print "ShevaSimilarity created"
        
    def __del__(self):
        print ' ShevaSimilarity destroyed'

    """
    MOVED TO SHEVADB
    #@profile
    def prepareComparisonDocuments(self, sqlQuery):

        Input: 
            sqlQuery to be executed, first parameter being textual data to convert to BoW
            
        Returns:
            BoW representation of documents returned from sqlQuery, list of lists

        #variables
        originalID = []
        bowReturn = []    
        
        #check sqlQuery
        if sqlQuery == "":
            sys.exit("No query mate @ ShevaLevelSIM.prepareComparisonDocuments()")
        elif type(sqlQuery) is str:
            sqlQueryResults = self.shevaDB.dbQuery(sqlQuery)
        elif type(sqlQuery) is tuple or type(sqlQuery) is list:
            sqlQueryResults = sqlQuery
        else:
            print type(sqlQuery)
            print "Error @ ShevaLevelSIM.prepareComparisonDocuments() "
            sys.exit(1)
            
        content= [[item for item in row[0].split()] for row in sqlQueryResults]
        bowReturn.extend(self.shevaTPF.returnClean(content))
        originalID = [row[1] for row in sqlQueryResults]
        return (bowReturn,originalID)
    """
    
    def getOriginalRowFromModel(self, modelRow, modelDocument):
        """
        Return document catid stored at modelRow row model file 
        """
        #variables
        originalRow = "Empty"
        #open csv
        f = open(modelDocument, "rb") # don't forget the 'b'!
        reader = csv.reader(f)
    
        #default
        for row in reader:
            #print row[0]
            if row[0] == str(modelRow):
                originalRow = row[1]
                f.close()
                return originalRow
        f.close()
        
    def checkIfExists(self):
        for groupingType in self.grouping:
            for testingDataItem in self.testData:
                path = "%s/%s/%s/" %(self.rootModelDir,groupingType,testingDataItem)
                fileName = "%s_%s_%s" %(testingDataItem,category,depth)
                fileNameRange =  "%s_%s_1_%s" %(testingDataItem,category,depth)
    
                #CHECK PATHS FOR SIM FILES 
                simPath = "%ssim/"%(path)    
                operationPath = "%s%s/" % (simPath,"SummaryCSV")
                limitPath = "%s%s/" % (operationPath,limit)
                resultsSavePathLevel = "%s%s.csv" %(limitPath,fileName)
                resultsSavePathRange = "%s%s.csv" %(limitPath,fileNameRange)    
                
                if not os.path.isfile(resultsSavePathLevel):
                    notAllDone = True
                    
                if not os.path.isfile(resultsSavePathRange):
                    notAllDone = True 

    #@profile
    def getSimilarityIndex(self,path, fileName, grouping):
        ####################        PATHS TO GENSIM FILES  ##########################
        #print "Started to calculate similarities"
        corpusPath = "%scorpus/%s.mm" % (path,fileName)
        dictPath = "%sdict/%s.dict" % (path,fileName)
        modelPath = "%smodels/%s.tfidf_model" % (path,fileName)
        indexDir = "%sindexFiles/" %(path)
        indexPath = "%sindexFiles/%s_%s.index" % (path, grouping, fileName)
    
        #open needed files
        corpus = gensim.corpora.MmCorpus(corpusPath)
        dictionary = gensim.corpora.Dictionary.load(dictPath)
        model = gensim.models.TfidfModel.load(modelPath)
        """
        print "corpus.num_docs:", corpus.num_docs
        print "corpus.num_terms:", corpus.num_terms
        print "corpus.num_nnz:", corpus.num_nnz
        """
        if os.path.exists(indexPath):
            #print "exists"
            index = gensim.similarities.Similarity.load(indexPath)
        else:
            #create index dir
            #self.shevaUtils.createDirOne(indexDir)
            tmpSim = 'tempSim/%s_%s' %(grouping, fileName)
            index = gensim.similarities.Similarity(tmpSim,model[corpus],num_features=len(dictionary))
            index.save(indexPath)
        
        #print "finished calculating similarities"
        return (index, model, dictionary, corpus.num_docs)
    
    #@profile
    def convert2VSM(self, data, VSM):
        """
        Convert data (as list of lists) to VSM (list of lists)
        INPUT: 
            data: BoW list of lists
            VSM: vector space model to convert BoW documents to
            treshold: get sim values greater than level (default 0)
        RETURN: 
            BoW in VSM
        """
        #print "started with vsm conversion"
        vsmConverted = []
        vsmConverted = [VSM[item] for item in data]
        #print "done with vsm conversion"
        return vsmConverted

    #@profile
    def calculateSimilarity(self, simIndex, data, treshold=0.1):
        """
        INPUT:
            simIndex: similarity index form comparison
            data: VSM representation of cleaned BoW data as list of lists
        RETURN:
            enumerated similarites with sim > treshold (default = 0.1)
        """
        #print "started similarity calucaltions"
        simarr = []
        
        #built in enumeration with best n documents returned
        simIndex.num_best = 1000
        #simIndex.chunksize=1
        """
        for similarities in simIndex[data]:
            #print similarities
            tmp = numpy.where(similarities > 0.1)[0]
            new_indices = tmp.take(numpy.argsort(similarities.take(tmp)))
            tmpSim = zip(new_indices, similarities.take(new_indices))[::-1]
    
            #tmpSim = [sim for sim in enumerate(similarities) if sim[1] > treshold]
            #tmpSim = sorted(tmpSim, key=lambda x: x[1], reverse=True)
            #print type(tmpSim)

            simarr.append(tmpSim)
            tmpSim = []
            
        """

        similarities = []
        tmpSim = []

        #a = 0
        for dox in data:
            #a += 1
            #print "Document nr ", a
            similarities = simIndex[dox]
            #print similarities
            tmpSim = [sim for sim in similarities if sim[1] > treshold]
            simarr.append(tmpSim)
            tmpSim = []
            similarities = []

        #print "Done with similarity calucaltions"
        return simarr
    
    def calculateSimilarityCumulative(self, simIndex, data, treshold=0.1):
        """
        INPUT:
            simIndex: similarity index form comparison
            data: VSM representation of cleaned BoW data as list of lists
        RETURN:
            cumulative similarity sum with sim > treshold (default = 0.1)
        """
        simarr = []
        
        #built in enumeration with best n documents returned
        simIndex.num_best = 1000
        similarities = []
        tmpSim = []

        for dox in data:
            tmpSim = []
            similarities = []
            similarities = simIndex[dox]
            tmpSim = [sim[1] for sim in similarities if sim[1] > treshold]
            if len(tmpSim) > 0:
                simarr.extend(tmpSim)
        return sum(simarr)


    #@profile
    def calculateSimilarityDocumentClassification(self, simIndex, data, treshold=0.0):
        """
        INPUT:
            simIndex: similarity index form comparison
            data: VSM representation of cleaned BoW data as list of lists
        RETURN:
            enumerated similarites with sim > treshold (default = 0.1)
        """
        #print "started similarity calucaltions"
        simarr = []
        
        #built in enumeration with best n documents returned
        simIndex.num_best = 1000
        #simIndex.chunksize=1
        """
        for similarities in simIndex[data]:
            #print similarities
            tmp = numpy.where(similarities > 0.1)[0]
            new_indices = tmp.take(numpy.argsort(similarities.take(tmp)))
            tmpSim = zip(new_indices, similarities.take(new_indices))[::-1]
    
            #tmpSim = [sim for sim in enumerate(similarities) if sim[1] > treshold]
            #tmpSim = sorted(tmpSim, key=lambda x: x[1], reverse=True)
            #print type(tmpSim)

            simarr.append(tmpSim)
            tmpSim = []
            
        """

        similarities = []
        tmpSim = []

        #a = 0
        for dox in data:
            #a += 1
            #print "Document nr ", a
            similarities = simIndex[dox]
            #print similarities
            tmpSim = [sim for sim in similarities if sim[1] > treshold]
            simarr.append(tmpSim)

        #print "Done with similarity calucaltions"
        return simarr

        
    #@profile
    def getOIDfromModel(self, path, fileName):
        iodPath = "%soriginalID/%s.csv" % (path,fileName)
        f = open(iodPath, "rb") # don't forget the 'b'!
        header = ["modelRowNumber","original_ID"]
        readerTemp = csv.DictReader(f,header)
        reader = {row['modelRowNumber']:row['original_ID'] for row in readerTemp}
        f.close()
        return reader
