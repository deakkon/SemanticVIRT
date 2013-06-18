'''
Created on 9.1.2013.

@author: Jurica Seva

PhD Candidate 
Faculty of Organization and Informatics
University of Zagreb
'''
#imports
import sys
import operator

#USER DEFINED MODULES
sys.path.append("/home/jseva/SemanticVIRT/_utils/")
from ShevaDB import ShevaDB
from ShevaTPF import ShevaTPF
from ShevaUtils import ShevaUtils
from ShevaVect import ShevaVect
from ShevaCSV import ShevaCSV
from ShevaSimilarity import ShevaSimilarity
from ShevaClassificationMetrics import ShevaClassificationMetrics

class SimilarityLevel:
    
    def __init__(self, type, testSize):
        """
        INPUT:
            type = full data (1) or training data (2)
            testSize = % of model size (nr of documents in model) to test with
        """
        #percentage of data to be used for model build
        if type == 1:
            self.GROUPTYPE = ["CATID","FATHERID","GENERAL"]
            self.percentageList = [25, 50, 75, 100]
        elif type == 2:
            self.GROUPTYPE = ["FATHERID"]
            self.percentageList = [25, 50, 75, 100]
        else:
            sys.exit("Wrong 'type' parameter in createData.__init__")
        
        #Sheva Objects
        self.shevaDB = ShevaDB()
        self.shevaTPF = ShevaTPF()
        self.shevaUtils = ShevaUtils()
        self.shevaVect = ShevaVect()
        self.shevaSimilarity = ShevaSimilarity()
        self.shevaCSV = ShevaCSV()
        self.shevaClassificationMetrics = ShevaClassificationMetrics()
        
        #SimilarityLevel Variables        
        self.rootDir = "LevelModels/"
        self.testSize = testSize
            
    def calculateLevelSimilarity(self, category):
        
        ranger = self.shevaDB.getCategoryDepth(category)
        dbData = self.shevaDB.getDBDocuments(category)

        for group in self.GROUPTYPE:
            print "####################################################################"
            for percentage in self.percentageList:
                print "####################################################################"
                for depth in ranger:
                    #variables
                    sim = []
                    vec_bow = []

                    print "####################################################################"
                    print category, group, percentage, depth
                    #path & csv file
                    path = "%s%s/%s/" %(self.rootDir,group,percentage)
                    fileName = "%s_%s_1_%s" %(percentage,category,depth)
                    IODfilePath = "%soriginalID/%s.csv" %(path,fileName)
                    #print IODfilePath
                    #get data from original ID csv; unique ID
                    allCategoryDataOID = self.shevaCSV.getModelCSV(IODfilePath)
                    categoryDataOID = self.shevaCSV.getIDfromModel(IODfilePath)

                    #different data for different grouping
                    if group != "FATHERID":
                        categoryData = [list(operator.itemgetter(0,1)(i)) for i in dbData if str(i[1]) in categoryDataOID]
                    else:
                        categoryData = [list(operator.itemgetter(0,2)(i)) for i in dbData if str(i[2]) in categoryDataOID]
                        
                    #get sim index, model, dict
                    index, tfidfModel, dictionary, corpusSize = self.shevaSimilarity.getSimilarityIndex(path,fileName)
                    
                    #return sample from original data
                    categoryDataOID, categoryData = self.shevaSimilarity.getSample(corpusSize,self.testSize,categoryData)
                    #print "Testing data size:\t", len(categoryData),"\t",len(categoryDataOID)

                    #calculate similarites
                    cleanText = self.shevaTPF.returnClean(categoryData,1)
                    contentLenght = range(0,len(cleanText))
                    vec_bow = [dictionary.doc2bow(cleanText[i]) for i in contentLenght]
                    vec_bow = self.shevaSimilarity.convert2VSM(vec_bow,tfidfModel)
                    sim = self.shevaSimilarity.calculateSimilarity(index,vec_bow,0.1)

                    #calcualte IR measures
                    cPrecision, cRecall, cF1 = self.shevaClassificationMetrics.computeClassificationMetrics(categoryDataOID, allCategoryDataOID, sim)
                    print "All data measures :\t\tPrecision:\t",cPrecision,"\t\tRecall\t",cRecall,"\t\tF1:\t",cF1
                    cPrecisionR, cRecallR, cF1R = self.shevaClassificationMetrics.computeClassificationMetricsRelative(categoryDataOID, allCategoryDataOID, sim)
                    print "Relative (with or) data measures :\t\tPrecision:\t",cPrecisionR,"\t\tRecall\t",cRecallR,"\t\tF1:\t",cF1R
                    cPrecisionE, cRecallE, cF1E = self.shevaClassificationMetrics.computeClassificationMetricsExclusive(categoryDataOID, allCategoryDataOID, sim)
                    print "Exclusive (with and) data measures :\t\tPrecision:\t",cPrecisionE,"\t\tRecall\t",cRecallE,"\t\tF1:\t",cF1E                    
                    
similarityLevel = SimilarityLevel(2,10)
similarityLevel.calculateLevelSimilarity("Arts")