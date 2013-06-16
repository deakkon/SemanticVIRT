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
import random

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
            self.GROUPTYPE = ["CATID","FATHERID","GENERAL"]
            self.percentageList = [25]
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
        ranger = ["2","3","4"]
        for group in self.GROUPTYPE:
            for percentage in self.percentageList:
                for depth in ranger:
                    print "####################################################################"
                    print category, group, percentage, depth
                    #path & csv file
                    path = "%s%s/%s/" %(self.rootDir,group,percentage)
                    fileName = "%s_%s_1_%s" %(percentage,category,depth)
                    IODfilePath = "%soriginalID/%s.csv" %(path,fileName)
                    print IODfilePath
                    #get data from original ID csv; unique ID
                    categoryDataOID = self.shevaCSV.getIDfromModel(IODfilePath)
                    
                    #different data for different grouping
                    if group != "FATHERID":
                        categoryData = [list(operator.itemgetter(0,1)(i)) for i in dbData if str(i[1]) in categoryDataOID]
                    else:
                        categoryData = [list(operator.itemgetter(0,2)(i)) for i in dbData if str(i[2]) in categoryDataOID]
                        
                    #get sim index, model, dict
                    index, tfidfModel, dictionary, corpusSize = self.shevaSimilarity.getSimilarityIndex(path,fileName)
                    
                    
                    #get sample size
                    print "CS:",corpusSize
                    sampleSize = int((self.testSize * corpusSize)/100)
                    print "SS:",sampleSize
                    if sampleSize == 0:
                        sampleSize = 1
                    
                    #get sample from all documents
                    if len(categoryData) > int(sampleSize):
                        #get random elements
                        indices = random.sample(xrange(len(categoryData)), int(sampleSize))
                        categoryData = [categoryData[i] for i in indices]
                        #random documents if nr of documents < than sampleSize 
                        categoryDataOID = [str(item[1]) for item in categoryData]
                        categoryData=[item[0].split() for item in categoryData]
                    else:
                        categoryDataOID = [str(item[1]) for item in categoryData]
                        categoryData=[item[0].split() for item in categoryData]

                    print "Testing data size:\t", len(categoryData),"\t",len(categoryDataOID)
                    
                    #calculate similarites
                    cleanText = self.shevaTPF.returnClean(categoryData,1)
                    contentLenght = range(0,len(cleanText))
                    vec_bow = []
                    for i in contentLenght:
                        vec_bow.append(dictionary.doc2bow(cleanText[i]))
                    vec_bow = self.shevaSimilarity.convert2VSM(vec_bow,tfidfModel)
                    sim = []
                    sim = self.shevaSimilarity.calculateSimilarity(index,vec_bow,0.4)
                    
                    #document ID in model
                    allCategoryDataOID = self.shevaCSV.getModelCSV(IODfilePath)

                    #input, output variables
                    returnedCategoryID = []      
                    lookingFor = []              
                    for comparisonDocumentID, row in zip(categoryDataOID, sim):
                        #print comparisonDocumentID, row
                        for item in row:
                            #print "Looking for: %s\t Found: %s\t Similarity:%s" %(comparisonDocumentID,allCategoryDataOID[str(item[0])],item[1])
                            lookingFor.append(comparisonDocumentID)
                            returnedCategoryID.append(allCategoryDataOID[str(item[0])])
                            
                    #print lookingFor
                    #print found
                    print "Input ID:\t ",len(lookingFor),"\tOutput ID:\t",len(returnedCategoryID)
                    if len(returnedCategoryID) > 0:
                        precision,recall, F1 =  self.shevaClassificationMetrics.computeClassificationMetrics(lookingFor,returnedCategoryID)
                        print "Precision:\t",precision
                        print "Recall\t",recall
                        print "F1:\t",F1
                    else:
                        print "Unable 2 compute since len(returnedCategoryID) = ", len(returnedCategoryID)
                        precision =recall = F1 = 0
                        print "Precision:\t",precision
                        print "Recall\t",recall
                        print "F1:\t",F1
                    
                    
                    #all rows in model
                    
                    #analyze results
                    #TO DO


                    
similarityLevel = SimilarityLevel(2,10)
similarityLevel.calculateLevelSimilarity("Arts")