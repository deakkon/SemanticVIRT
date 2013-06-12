#imports
import sys

#USER DEFINED MODULES
sys.path.append("/home/jseva/SemanticVIRT/_utils/")
from ShevaDB import ShevaDB
from ShevaTPF import ShevaTPF
from ShevaUtils import ShevaUtils
from ShevaVect import ShevaVect

#SYS IMPORTS
import gensim
import csv

class ShevaSimilarity:
    
    def __init__(self):
        self.shevaDB = ShevaDB()
        self.shevaTPF = ShevaTPF()
        self.shevaUtils = ShevaUtils()
        self.shevaVect = ShevaVect()

    def prepareComparisonDocuments(self, sqlQuery):
        """
        Input: 
            sqlQuery to be executed, first parameter being textual data to convert to BoW
            
        Output parameters:
            BoW representation of documents returned from sqlQuery, list of lists
        """
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
        
    def getSimilarityIndex(self,path,fileName):
        
        ####################        PATHS TO GENSIM FILES  ##########################
        corpusPath = "%scorpus/%s.mm" % (path,fileName)
        dictPath = "%sdict/%s.dict" % (path,fileName)
        modelPath = "%smodels/%s.tfidf_model" % (path,fileName)
    
        #open needed files
        corpus = gensim.corpora.MmCorpus(corpusPath)
        dictionary = gensim.corpora.Dictionary.load(dictPath)
        model = gensim.models.TfidfModel.load(modelPath)
        
        #create similartiy index depending on the nr of unique tokens of corpus
        if corpus.num_terms < 25000:
            index = gensim.similarities.MatrixSimilarity(model[corpus],num_features=len(dictionary))
        else:
            tmpSim = 'tempSim/%s' %(fileName)
            index = gensim.similarities.Similarity(tmpSim,model[corpus],num_features=len(dictionary))
            
        return (index, model, dictionary)
    
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
        vsmConverted = []
        vsmConverted = [VSM[item] for item in data]
        return vsmConverted

    def calculateSimilarity(self, simIndex, data, treshold=0.1):
        """
        INPUT:
            simIndex: similarity index form comparison
            data: VSM representation of cleaned BoW data as list of lists
        RETURN:
            enumerated similarites with sim > treshold (default = 0.1)
        """
        simarr = []

        for similarities in simIndex[data]:
            #print type(similarities)
            similarities = enumerate(similarities)
            tmpSim = [sim for sim in similarities if sim[1] > treshold]
            #print type(tmpSim)
            #print len(tmpSim),"\t",tmpSim,"\n"
            simarr.append(tmpSim)
        return simarr
    
    def getOIDfromModel(self, path, fileName):
        iodPath = "%soriginalID/%s.csv" % (path,fileName)
        f = open(iodPath, "rb") # don't forget the 'b'!
        header = ["modelRowNumber","original_ID"]
        readerTemp = csv.DictReader(f,header)
        reader = {row['modelRowNumber']:row['original_ID'] for row in readerTemp}
        f.close()
        return reader