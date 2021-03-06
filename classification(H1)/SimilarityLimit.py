'''
Created on 9.1.2013.

@author: Jurica Seva

PhD Candidate 
Faculty of Organization and Informatics
University of Zagreb
'''
#imports
import sys
import pp
import gc
import time
import weakref
import pprint
#gc.set_debug(gc.DEBUG_LEAK)

#USER DEFINED MODULES
sys.path.append("/home/jseva/SemanticVIRT/_utils/")
from ShevaDB import ShevaDB
from ShevaCSV import ShevaCSV
from ShevaTPF import ShevaTPF
from ShevaSimilarity import ShevaSimilarity
from ShevaClassificationMetrics import ShevaClassificationMetrics
from ShevaUtils import ShevaUtils

class SimilarityLimit:   
    ##@profile w
    def __init__(self, testSize, category, type=1):
        """
        INPUT:
            type = full data (1) or training data (2)
            testSize = % of model size (nr of documents in model) to test with
        """

        #percentage of data to be used for model build
        if type == 1:
            self.GROUPTYPE = ["CATID", "FATHERID", "GENERAL"]
            self.limitList = [1000, 2500, 5000, 7500, 10000, 20000]
        elif type == 2:
            self.GROUPTYPE = ["GENERAL", "FATHERID", "GENERAL"]
            self.limitList = [1000]
        else:
            sys.exit("Wrong 'type' parameter in createData.__init__")

        print "SimilarityLevel created"
        #Sheva Objects
        self.shevaDB = ShevaDB()
        self.shevaTPF = ShevaTPF()
        self.shevaSimilarity =  ShevaSimilarity()
        self.shevaCSV =  ShevaCSV()
        self.shevaClassificationMetrics =  ShevaClassificationMetrics()
        self.shevaUtils =  ShevaUtils()
        
        #SimilarityLevel Variables        
        self.rootDir = "LimitModels/"
        self.testSize = testSize
        self.category = category
        self.maxDepth = self.shevaDB.getCategorymaxDepth(self.category)

    def __del__(self):
        print 'SimilarityLevel destroyed'                  
            
    #@profile
    def calculateLimitSimilarity(self):

        for limit in self.limitList:            
            for group in self.GROUPTYPE:
                print "####################################################################"
                #print category, group, percentage, debth

                sim = []
                vec_bow = []
                allCategoryDataOID = []
                categoryDataOID = []
                categoryData = []
                print "created variables"
                 
                #path & csv file
                path = "%s%s/%s/" %(self.rootDir,group,limit)
                fileName = "%s_%s" %(limit,self.category)
                IODfilePath = "%soriginalID/%s.csv" %(path,fileName)
                print "Setup paths"
                
                #get data from original ID csv; unique ID
                allCategoryDataOID = self.shevaCSV.getModelCSV(IODfilePath)
                #categoryDataOID = self.shevaCSV.getIDfromModel(IODfilePath)
                print "Got all modelRow->originalID mappings"
        
                #get sim index, model, dict
                indexDir = "%sindexFiles/" %(path)
                self.shevaUtils.createDirOne(indexDir)
                index, tfidfModel, dictionary, corpusSize = self.shevaSimilarity.getSimilarityIndex(path, fileName, group)
                #return sample from original data
                categoryDataOID, categoryData = self.shevaDB.getSample(limit,self.testSize,self.category,self.maxDepth, group)
        
                #calculate similarites
                cleanText = self.shevaTPF.returnClean(categoryData, 1)
                cleanTextBoW = [dictionary.doc2bow(cleanText[i]) for i in range(0, len(cleanText))]
                print "Done with bow representation"
                vec_bow = self.shevaSimilarity.convert2VSM(cleanTextBoW, tfidfModel)
                print len(vec_bow)
                
                simCalculation = self.shevaSimilarity.calculateSimilarity(index, vec_bow, 0.1)
        
                #calcualte IR measures
                cPrecision, cRecall, cF1 = self.shevaClassificationMetrics.computeClassificationMetrics(categoryDataOID, allCategoryDataOID, simCalculation)
                print "All data measures :\t\t\t\tPrecision:\t", cPrecision, "\t\tRecall\t", cRecall, "\t\tF1:\t", cF1
                sqlClassic = "INSERT INTO analysis_results_limit (category, groupingType, limitValue, levelDepth, testSize, measureType, P, R, F1) VALUES ('%s', '%s', '%s', '%i', '%i', '%s','%f','%f','%f')" % (self.category,group,limit,self.maxDepth,self.testSize, "computeClassificationMetrics",cPrecision, cRecall, cF1)
                self.shevaDB.dbQuery(sqlClassic)
        
                cPrecisionR, cRecallR, cF1R = self.shevaClassificationMetrics.computeClassificationMetricsRelative(categoryDataOID, allCategoryDataOID, simCalculation)
                print "Relative (with or) data measures :\t\tPrecision:\t", cPrecisionR, "\t\tRecall\t", cRecallR, "\t\tF1:\t", cF1R
                sqlRelative = "INSERT INTO analysis_results_limit (category, groupingType, limitValue, levelDepth, testSize,measureType, P, R, F1) VALUES ('%s', '%s', '%s', '%i', '%i', '%s','%f','%f','%f')" % (self.category,group,limit,self.maxDepth,self.testSize, "computeClassificationMetricsRelative",cPrecisionR, cRecallR, cF1R)
                self.shevaDB.dbQuery(sqlRelative)
                
                cPrecisionE, cRecallE, cF1E = self.shevaClassificationMetrics.computeClassificationMetricsExclusive(categoryDataOID, allCategoryDataOID, simCalculation)
                print "Exclusive (with and) data measures :\t\tPrecision:\t", cPrecisionE, "\t\tRecall\t", cRecallE, "\t\tF1:\t", cF1E
                sqlExclusive = "INSERT INTO analysis_results_limit (category, groupingType, limitValue, levelDepth,testSize, measureType, P, R, F1) VALUES ('%s', '%s', '%s', '%i', '%i', '%s','%f','%f','%f')" % (self.category,group,limit,self.maxDepth,self.testSize, "computeClassificationMetricsExclusive",cPrecisionE, cRecallE, cF1E)
                self.shevaDB.dbQuery(sqlExclusive)
        
                #trying to figure out the memory thing. needs speed-up in performance otherwise... 
                dbData = []
                simCalculation = []
                cleanText = []
                cleanTextBoW = []
                vec_bow = []
                
                del index
                del tfidfModel
                del dictionary
                del corpusSize
                del simCalculation
                del vec_bow
                del allCategoryDataOID
                del categoryDataOID
                del categoryData
                del dbData
                gc.collect()



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
jobs = []
inputs = ShevaDB().getMainCat()
#percentageList = [100, 75, 50, 25]
#GROUPTYPE = ["CATID", "FATHERID", "GENERAL"]
#inputs = ["Regional", "Arts"]

for category in inputs:
    similarityLimit = SimilarityLimit(10, category)
    jobs.append(job_server.submit(similarityLimit.calculateLimitSimilarity, (), depfuncs = (), modules = ("gc","time","pp","time","sys","operator","SimilarityLevel","ShevaClassificationMetrics","ShevaDB","ShevaTPF","ShevaCSV","ShevaSimilarity")))
    #print "Queing: ",category

for i in xrange(len(jobs)):
    jobs[i]()    
    jobs[i] = ''

#prints
job_server.print_stats()
print "Time elapsed: ", time.time() - start_time, "s"
"""

#testing initialization
start_time = time.time()
percentageList = [25, 50, 75, 100]
GROUPTYPE = ["CATID", "FATHERID", "GENERAL"]
inputs = ShevaDB().getMainCat()
#inputs = ["News"]
for category in inputs:
    ranger = ShevaDB().getCategorymaxDepth(category)  
    #ranger = 3  
    for group in GROUPTYPE:
        for p in percentageList:
            if ShevaDB().getNumberOfRows(category, group, p, ranger) == 0:
                similarityLevel =  SimilarityLevel(10)
                similarityLevel.calculateLevelSimilarity(category, ranger, p, group)
                del similarityLevel
                gc.collect()
            
print "Time elapsed: ", time.time() - start_time, "s"
"""