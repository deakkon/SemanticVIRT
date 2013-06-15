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
    
    def __init__(self, type, sampleSize):
        #percentage of data to be used for model build
        if type == 1:
            self.GROUPTYPE = ["CATID","FATHERID","GENERAL"]
            self.percentageList = [25, 50, 75, 100]
        elif type == 2:
            self.GROUPTYPE = ["GENERAL"]
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
        self.sampleSize = sampleSize
            
    def calculateLevelSimilarity(self, category):
        
        ranger = self.shevaDB.getCategoryDepth(category)
        dbData = self.shevaDB.getDBDocuments(category)

        for group in self.GROUPTYPE:
            for percentage in self.percentageList:
                for depth in ranger:
                    print "####################################################################"
                    print category, group, percentage, depth
                    #path & csv file
                    path = "%s%s/%s/" %(self.rootDir,group,percentage)
                    fileName = "%s_%s_1_%s" %(percentage,category,depth)
                    IODfilePath = "%soriginalID/%s.csv" %(path,fileName)
                    
                    #get data from original ID csv; unique ID
                    categoryDataOID = self.shevaCSV.getIDfromModel(IODfilePath)
                    
                    #different data for different grouping
                    if group != "FATHERID":
                        categoryData = [list(operator.itemgetter(0,1)(i)) for i in dbData if str(i[1]) in categoryDataOID]
                    else:
                        categoryData = [list(operator.itemgetter(0,2)(i)) for i in dbData if str(i[2]) in categoryDataOID]
                                        
                    #get sample
                    if len(categoryData) > int(self.sampleSize):
                        #get random elements
                        indices = random.sample(xrange(len(categoryData)), int(self.sampleSize))
                        categoryData = [categoryData[i] for i in indices]
                        #random documents if nr of documents < than sampleSize 
                        categoryDataOID = [str(item[1]) for item in categoryData]
                        categoryData=[item[0].split() for item in categoryData]
                    else:
                        categoryData=[item[0].split() for item in categoryData]

                    #calcualte similarites
                    cleanText = self.shevaTPF.returnClean(categoryData,1)    
                    index, tfidfModel, dictionary = self.shevaSimilarity.getSimilarityIndex(path,fileName)
                    contentLenght = range(0,len(cleanText))
                    vec_bow = []
                    for i in contentLenght:
                        vec_bow.append(dictionary.doc2bow(cleanText[i]))
                    vec_bow = self.shevaSimilarity.convert2VSM(vec_bow,tfidfModel)
                    sim = []
                    sim = self.shevaSimilarity.calculateSimilarity(index,vec_bow)
                    
                    #document ID in model
                    allCategoryDataOID = self.shevaCSV.getModelCSV(IODfilePath)
                    
                    #input, output variables
                    lookingFor = []
                    found = []
                    
                    for comparisonDocumentID, row in zip(categoryDataOID, sim):
                        #print comparisonDocumentID, row
                        for item in row:
                            #print "Looking for: %s\t Found: %s\t Similarity:%s" %(comparisonDocumentID,allCategoryDataOID[str(item[0])],item[1])
                            lookingFor.append(comparisonDocumentID)
                            found.append(allCategoryDataOID[str(item[0])])
                    
                    precision,recall, F1 =  self.shevaClassificationMetrics.computeClassificationMetrics(lookingFor,found)
                    print "Precision:\t",precision
                    print "Recall\t",recall
                    print "F1:\t",F1
                    
                    
                    #all rows in model
                    
                    #analyze results
                    #TO DO

                    
similarityLevel = SimilarityLevel(2,10)
similarityLevel.calculateLevelSimilarity("Arts")