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
import pp
import gc
import time

#USER DEFINED MODULES
sys.path.append("/home/jseva/SemanticVIRT/_utils/")
from ShevaDB import ShevaDB
from ShevaCSV import ShevaCSV
from ShevaTPF import ShevaTPF
from ShevaVect import ShevaVect
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
            #self.percentageList = [25, 50, 75, 100]
        elif type == 2:
            self.GROUPTYPE = ["GENERAL"]
            #self.percentageList = [25, 50, 75, 100]
        else:
            sys.exit("Wrong 'type' parameter in createData.__init__")
        
        #Sheva Objects
        self.shevaDB = ShevaDB()
        self.shevaTPF = ShevaTPF()
        #self.shevaUtils = ShevaUtils()
        #self.shevaVect = ShevaVect()
        self.shevaSimilarity = ShevaSimilarity()
        self.shevaCSV = ShevaCSV()
        self.shevaClassificationMetrics = ShevaClassificationMetrics()
        
        #SimilarityLevel Variables        
        self.rootDir = "LevelModels/"
        self.testSize = testSize
            
    #@profile
    def calculateLevelSimilarity(self, category, debth, percentage):        

        dbData = self.shevaDB.getDBDocumentsDepth(category,debth)

        for group in self.GROUPTYPE:
            print "####################################################################"
#            start = time.time()
#            print "Start: ", start
            #for percentage in self.percentageList:

            sim = []
            vec_bow = []
            allCategoryDataOID = []
            categoryDataOID = []
            categoryData = []

            print category, group, percentage, debth
            #path & csv file
            path = "%s%s/%s/" %(self.rootDir,group,percentage)
            fileName = "%s_%s_1_%s" %(percentage,category,str(debth))
            IODfilePath = "%soriginalID/%s.csv" %(path,fileName)

            #get data from original ID csv; unique ID
            allCategoryDataOID = self.shevaCSV.getModelCSV(IODfilePath)
            categoryDataOID = self.shevaCSV.getIDfromModel(IODfilePath)

            #different data for different grouping
            if group != "FATHERID":
                categoryData = [list(operator.itemgetter(0,1)(i)) for i in dbData]
            else:
                categoryData = [list(operator.itemgetter(0,2)(i)) for i in dbData]
             
            #get sim index, model, dict
            index, tfidfModel, dictionary, corpusSize = self.shevaSimilarity.getSimilarityIndex(path,fileName)
            
            #return sample from original data
            categoryDataOID, categoryData = self.shevaSimilarity.getSample(corpusSize,self.testSize,categoryData)

            #calculate similarites
            cleanText = self.shevaTPF.returnClean(categoryData,1)
            contentLenght = range(0,len(cleanText))
            vec_bow = [dictionary.doc2bow(cleanText[i]) for i in contentLenght]
            vec_bow = self.shevaSimilarity.convert2VSM(vec_bow,tfidfModel)
            sim = self.shevaSimilarity.calculateSimilarity(index,vec_bow,0.1)

            #calcualte IR measures
            cPrecision, cRecall, cF1 = self.shevaClassificationMetrics.computeClassificationMetrics(categoryDataOID, allCategoryDataOID, sim)
            print "All data measures :\t\t\t\tPrecision:\t",cPrecision,"\t\tRecall\t",cRecall,"\t\tF1:\t",cF1
            sqlClassic = "INSERT INTO analysis_results (category, groupingType, limitValue, levelDepth, testSize, measureType, P, R, F1) VALUES ('%s', '%s', '%s', '%i', '%i', '%s','%f','%f','%f')" %(category,group,percentage,debth,self.testSize, "computeClassificationMetrics",cPrecision, cRecall, cF1)
            #print sqlClassic  
            self.shevaDB.dbQuery(sqlClassic)
    
            cPrecisionR, cRecallR, cF1R = self.shevaClassificationMetrics.computeClassificationMetricsRelative(categoryDataOID, allCategoryDataOID, sim)
            print "Relative (with or) data measures :\t\tPrecision:\t",cPrecisionR,"\t\tRecall\t",cRecallR,"\t\tF1:\t",cF1R
            sqlRelative = "INSERT INTO analysis_results (category, groupingType, limitValue, levelDepth, testSize,measureType, P, R, F1) VALUES ('%s', '%s', '%s', '%i', '%i', '%s','%f','%f','%f')" %(category,group,percentage,debth,self.testSize, "computeClassificationMetricsRelative",cPrecisionR, cRecallR, cF1R)
            self.shevaDB.dbQuery(sqlRelative)
            
            cPrecisionE, cRecallE, cF1E = self.shevaClassificationMetrics.computeClassificationMetricsExclusive(categoryDataOID, allCategoryDataOID, sim)
            print "Exclusive (with and) data measures :\t\tPrecision:\t",cPrecisionE,"\t\tRecall\t",cRecallE,"\t\tF1:\t",cF1E
            sqlExclusive = "INSERT INTO analysis_results (category, groupingType, limitValue, levelDepth,testSize, measureType, P, R, F1) VALUES ('%s', '%s', '%s', '%i', '%i', '%s','%f','%f','%f')" %(category,group,percentage,debth,self.testSize, "computeClassificationMetricsExclusive",cPrecisionE, cRecallE, cF1E)
            self.shevaDB.dbQuery(sqlExclusive)

            del index
            del tfidfModel
            del dictionary
            del corpusSize
            del sim
            del vec_bow
            del allCategoryDataOID
            del categoryDataOID
            del categoryData
            gc.collect()
        del dbData
        del self.shevaDB
        del self.shevaTPF
        del self.shevaSimilarity
        del self.shevaClassificationMetrics
        del self.shevaCSV
        gc.collect()

"""
#testing initialization
ranger = ShevaDB().getCategoryDepth("Arts")
percentageList = [25, 50, 75, 100]
ranger = [2,3,4,5]
for i in ranger:
    for p in percentageList:
        similarityLevel = SimilarityLevel(1,10)        
        similarityLevel.calculateLevelSimilarity("Arts",i,p)
"""
#PARALLEL PYTHON IMPLEMENTATION
ppservers = ()

if len(sys.argv) > 1:
    ncpus = int(sys.argv[1])
    # Creates jobserver with ncpus workers
    job_server = pp.Server(ncpus, ppservers=ppservers)
else:
    # Creates jobserver with automatically detected number of workers
    job_server = pp.Server(ppservers=ppservers)

print "Starting pp with", job_server.get_ncpus(), "workers"
start_time = time.time()

#start PP[]
GROUPTYPE = ["CATID","FATHERID","GENERAL"]
jobs = []
inputs = ShevaDB().getMainCat()
percentageList = [25, 50, 75, 100]

for category in inputs:
    ranger = ShevaDB().getCategoryDepth(category)
    for level in ranger:
        print "Queing: ",category,"\t",level
        for p in percentageList:
            similarityLevel = SimilarityLevel(1,10)
            jobs.append(job_server.submit(similarityLevel.calculateLevelSimilarity, 
                                          (category,level,p),
                                          depfuncs = (),
                                          modules = ("gc","time","pp","time","sys","operator","SimilarityLevel","ShevaClassificationMetrics","ShevaDB","ShevaTPF","ShevaCSV","ShevaSimilarity")))
            #del similarityLevel
            gc.collect()

for i in xrange(len(jobs)):
    jobs[i]()
    jobs[i] = ''     

"""
for job in jobs:
    result = job()
    jobs[i] = ''
    if result:
        break
"""
#prints
job_server.print_stats()
print "Time elapsed: ", time.time() - start_time, "s"