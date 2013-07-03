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

#USER DEFINED MODULES
sys.path.append("/home/jseva/SemanticVIRT/_utils/")
from ShevaDB import ShevaDB
from ShevaCSV import ShevaCSV
from ShevaTPF import ShevaTPF
from ShevaSimilarity import ShevaSimilarity
from ShevaClassificationMetrics import ShevaClassificationMetrics

class SimilarityLevel:   
    #@profile 
    def __init__(self, type, testSize):
        """
        INPUT:
            type = full data (1) or training data (2)
            testSize = % of model size (nr of documents in model) to test with
        """
        #percentage of data to be used for model build
        if type == 1:
            self.GROUPTYPE = ["CATID", "FATHERID", "GENERAL"]
            #self.percentageList = [25, 50, 75, 100]
        elif type == 2:
            self.GROUPTYPE = ["GENERAL"]
            #self.percentageList = [25, 50, 75, 100]
        else:
            sys.exit("Wrong 'type' parameter in createData.__init__")
        
        #Sheva Objects
        self.shevaDB = ShevaDB()
        self.shevaTPF = ShevaTPF()
        self.shevaSimilarity = ShevaSimilarity()
        self.shevaCSV = ShevaCSV()
        self.shevaClassificationMetrics = ShevaClassificationMetrics()
        
        #SimilarityLevel Variables        
        self.rootDir = "LevelModels/"
        self.testSize = testSize
            
    #@profile
    def calculateLevelSimilarity(self, category, debth, percentage, group):

        #dbData = self.shevaDB.getDBDocumentsDepth(category,debth)

        #for group in self.GROUPTYPE:
        print "####################################################################"
        print category, group, percentage, debth

        sim = []
        vec_bow = []
        allCategoryDataOID = []
        categoryDataOID = []
        categoryData = []

        #path & csv file
        path = "%s%s/%s/" %(self.rootDir,group,percentage)
        fileName = "%s_%s_1_%s" %(percentage,category,str(debth))
        IODfilePath = "%soriginalID/%s.csv" %(path,fileName)

        #get data from original ID csv; unique ID
        allCategoryDataOID = self.shevaCSV.getModelCSV(IODfilePath)
        #categoryDataOID = self.shevaCSV.getIDfromModel(IODfilePath)

        #get sim index, model, dict
        index, tfidfModel, dictionary, corpusSize = self.shevaSimilarity.getSimilarityIndex(path, fileName, group)
        
        #return sample from original data
        categoryDataOID, categoryData = self.shevaDB.getSample(corpusSize, self.testSize, category, debth, group)

        #calculate similarites
        cleanText = self.shevaTPF.returnClean(categoryData, 1)
        cleanTextBoW = [dictionary.doc2bow(cleanText[i]) for i in range(0, len(cleanText))]
        vec_bow = self.shevaSimilarity.convert2VSM(cleanTextBoW, tfidfModel)
        simCalculation = self.shevaSimilarity.calculateSimilarity(index, vec_bow, 0.1)
        
        print "cleanText: ", sys.getsizeof(cleanText)
        print "cleanTextBoW: ", sys.getsizeof(cleanTextBoW)
        print "vec_bow: ", sys.getsizeof(vec_bow)
        print "simCalculation: ", sys.getsizeof(simCalculation)
        
        #calcualte IR measures
        cPrecision, cRecall, cF1 = self.shevaClassificationMetrics.computeClassificationMetrics(categoryDataOID, allCategoryDataOID, simCalculation)
        print "All data measures :\t\t\t\tPrecision:\t", cPrecision, "\t\tRecall\t", cRecall, "\t\tF1:\t", cF1
        sqlClassic = "INSERT INTO analysis_results (category, groupingType, limitValue, levelDepth, testSize, measureType, P, R, F1) VALUES ('%s', '%s', '%s', '%i', '%i', '%s','%f','%f','%f')" % (category,group,percentage,debth,self.testSize, "computeClassificationMetrics",cPrecision, cRecall, cF1)
        self.shevaDB.dbQuery(sqlClassic)

        cPrecisionR, cRecallR, cF1R = self.shevaClassificationMetrics.computeClassificationMetricsRelative(categoryDataOID, allCategoryDataOID, simCalculation)
        print "Relative (with or) data measures :\t\tPrecision:\t", cPrecisionR, "\t\tRecall\t", cRecallR, "\t\tF1:\t", cF1R
        sqlRelative = "INSERT INTO analysis_results (category, groupingType, limitValue, levelDepth, testSize,measureType, P, R, F1) VALUES ('%s', '%s', '%s', '%i', '%i', '%s','%f','%f','%f')" % (category,group,percentage,debth,self.testSize, "computeClassificationMetricsRelative",cPrecisionR, cRecallR, cF1R)
        self.shevaDB.dbQuery(sqlRelative)
        
        cPrecisionE, cRecallE, cF1E = self.shevaClassificationMetrics.computeClassificationMetricsExclusive(categoryDataOID, allCategoryDataOID, simCalculation)
        print "Exclusive (with and) data measures :\t\tPrecision:\t", cPrecisionE, "\t\tRecall\t", cRecallE, "\t\tF1:\t", cF1E
        sqlExclusive = "INSERT INTO analysis_results (category, groupingType, limitValue, levelDepth,testSize, measureType, P, R, F1) VALUES ('%s', '%s', '%s', '%i', '%i', '%s','%f','%f','%f')" % (category,group,percentage,debth,self.testSize, "computeClassificationMetricsExclusive",cPrecisionE, cRecallE, cF1E)
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
        del sim
        del vec_bow
        del allCategoryDataOID
        del categoryDataOID
        del categoryData
        del dbData
        del self.shevaDB
        del self.shevaTPF
        del self.shevaSimilarity
        del self.shevaClassificationMetrics
        del self.shevaCSV
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
percentageList = [25, 50, 75, 100]
GROUPTYPE = ["CATID", "FATHERID", "GENERAL"]
#inputs = ["Arts"]

for category in inputs:
    ranger = ShevaDB().getCategorymaxDepth(category)    
    for group in GROUPTYPE:
        #ranger = ShevaDB().getCategoryDepth(category)
        #print ranger
        #for level in ranger:
        for p in percentageList:
            similarityLevel = SimilarityLevel(1,10)
            jobs.append(job_server.submit(similarityLevel.calculateLevelSimilarity, 
                                          (category,ranger,p,group),
                                          depfuncs = (),
                                          modules = ("gc","time","pp","time","sys","operator","SimilarityLevel","ShevaClassificationMetrics","ShevaDB","ShevaTPF","ShevaCSV","ShevaSimilarity")))
            print "Queing: ",category,"\t",ranger,"\t",p

for i in xrange(len(jobs)):
    jobs[i]()    
    jobs[i] = ''

#prints
job_server.print_stats()
print "Time elapsed: ", time.time() - start_time, "s"          

"""
#testing initialization
ranger = ShevaDB().getCategorymaxDepth("Regional")
percentageList = [25, 50, 75, 100]
GROUPTYPE = ["CATID", "FATHERID", "GENERAL"]
for group in GROUPTYPE:
    for p in percentageList:
        similarityLevel = SimilarityLevel(1, 10)
        similarityLevel.calculateLevelSimilarity("Regional", ranger, p, group)
"""