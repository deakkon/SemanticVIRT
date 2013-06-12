#SYSTEM MODULES
import sys
import os
import pp
import time
import string
import gc

#USER DEFINED MODULES
sys.path.append("/home/jseva/SemanticVIRT/_utils/")
from ShevaDB import ShevaDB
from ShevaSimilarity import ShevaSimilarity
#from ShevaTPF import ShevaTPF
#from ShevaUtils import ShevaUtils
#from ShevaVect import ShevaVect

class ShevaLevelSIM:
    
    def __init__(self, root, type):
        """
        Test models based on depth level delimiter. Not sure why.
        type: 1    -> full data
              2    -> test data, for testing purposes
        """
        self.rootModelDir = root
        self.shevaDB = ShevaDB()
        self.shevaSimilarity = ShevaSimilarity()
        #self.shevaTPF = ShevaTPF()
        #self.shevaUtils = ShevaUtils()
        #self.shevaVect = ShevaVect()
        
        if type == 1:
            self.testData = [25,50,75,100]
            self.grouping = ['GENERAL','CATID','FATHERID']
            self.limit = 1000
        elif type == 2:
            self.testData = [25]
            self.grouping = ['GENERAL']
            self.limit = 100
        else:
            sys.exit("ShevaLevelSIM.__init__: wrong 'type' value.")

    def calculateSimilarity(self,path,fileName,originalContent,originalId,category,depth,limit,groupingType):

        try:
            start_time = time.time()
            print start_time,": Started with %s on level %s in grouping %s: %s " %(category,depth,groupingType,fileName)

            ###################        GENSIM FILES           ##########################
            index,tfidfModel,dictionary = self.shevaSimilarity.getSimilarityIndex(path)
            
            ###################        CONVERT COTENT TO MODEL     #####################
            originalContent = shevaSimilarity.convert2VSM(originalContent,tfidfModel)
            
            ###################        CALCULATE SIMILARITY        #####################
            similarities = shevaSimilarity.calculateSimilarity(index,originalContent)

            ####################        PATHS TO FILES         ##########################
            simPath = "%ssim/"%(path)
            resultsSavePath = "%s%s.csv" %(simPath,fileName)
            oidSavePath = "%s%s_queryOID.csv" %(path,fileName)
            oidSavePathRelative = "%s%s_RelativeSim.csv" %(path,fileName)
    
            #create dict, sort, filter, write to either db or csv
            dictAnalysis = {}
            dictRelative = []
            originalIDList = []
            
            ####################        ORIGINAL CATID FROM MODEL
            oidCSV = shevaSimilarity.getOIDfromModel(path,fileName)
            
            """
            modelID = "%soriginalID/%s.csv" % (path,fileName)
            f = open(modelID, "rb") # don't forget the 'b'!
            header = ["number of row in model","original cat id"]
            readerTemp = csv.DictReader(f,header)
            reader = {row['number of row in model']:row['original cat id'] for row in readerTemp}
            f.close()
            """

        
            #print "OC:\t",len(originalContent),originalContent 
            #print "OID:\t",len(originalId),originalId
            #similarities for list of documents
            """
            for descriptionLevel, idLevel in  itertools.izip(originalContent,originalId):
                #relative sim value initial states
                sumTemp = float()
                simFound = float()
                relativeSum = float()
                #prepare documents and calculate similarity
                vec_bow = dictionary.doc2bow(descriptionLevel)
                vec_tfidf = tfidfModel[vec_bow]
                sims = []
                sims = index[vec_tfidf]
                #print "Sims:\t",len(sims),"\t",sims,"\t",descriptionLevel,"\t",descriptionLevel,"\t",idLevel
                sims = enumerate(sims)
                #print "Sims:\t",len(sims),"\t",sims
                
                sims = [x for x in sims if x[1] > 0]
                #print "Sims:\t",len(sims),"\t",sims
            """
            #summarization: for individual dox, go through all similar documents from model and add to dictionary
            for sim in sims:
                originalID_item=reader[str(sim[0])]
                sumTemp += sim[1]
                #summary CSV data
                if sim[0] in dictAnalysis:
                    dictAnalysis[sim[0]]['nrOcc'] += 1
                    dictAnalysis[sim[0]]['sim']+=sim[1]
                else:
                    #originalIDtTem=reader[str(sim[0])]
                    dictAnalysis[sim[0]] = {'category': category, 'depth': depth, 'idLevel': idLevel, 'ocID': int(originalID_item), 'sim':sim[1], 'nrOcc': 1}

                if originalID_item == str(idLevel):
                    simFound += sim[1]

            if sumTemp > 0:
                relativeSum = simFound/sumTemp
                dictRelative.append((idLevel,relativeSum))
            #else:
                #dictRelative.append((idLevel,0))
        
            #sort dictionary by sum value and write to CSV -> write cumulative similarity measures
            dictAnalysisValues = sorted(dictAnalysis.values(),key=lambda k: k['nrOcc'], reverse=True)
            keys = ['category', 'depth','idLevel','ocID','sim','nrOcc']
            f = open(resultsSavePath, 'wb')
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writer.writerow(keys)
            dict_writer.writerows(dictAnalysisValues)
            f.close()
            
            #create relative summary files
            with open(oidSavePathRelative, "wb") as the_file:
                keys = ['catID', 'relSim']
                csv.register_dialect("custom", delimiter=",", skipinitialspace=True,)
                writerRelative = csv.DictWriter(the_file, keys)
                writerRelative.writer.writerow(keys)
                for item in dictRelative:
                    writerRelative.writer.writerow(item)
    
            #write original id's
            myfile = open(oidSavePath, 'wb')
            wr = csv.writer(myfile, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
            wr.writerow(['OID'])
    
            for x in originalId:
                wr.writerow([x])
            
            myfile.close()
        
            #CSV for summary (nr of returned sim rows vs nr of rows submitted)
            summaryCSVPath = "%ssummary_%s.csv" % (path,limit)
            if not os.path.exists(summaryCSVPath):
                summaryFile  = open(summaryCSVPath, "wb")
                csvSummary = csv.writer(summaryFile, delimiter=',', quotechar='"',quoting=csv.QUOTE_ALL)
                csvSummary.writerow(("Category","Level","Model","docsInModel","ReturnedDocsForModel","NrInputDocs"))
            else:
                summaryFile = open(summaryCSVPath,'a')
                csvSummary = csv.writer(summaryFile, delimiter=',', quotechar='"',quoting=csv.QUOTE_ALL)
            
            summarySTR = [category,depth,fileName,tfidfModel.num_docs,len(dictAnalysis),len(originalContent)] 
            csvSummary.writerow(summarySTR)
            summaryFile.close()
        
            logText = 'Finished calculating similarity for %s, %s ; simFile: %s '%(category,depth,resultsSavePath)
            logging.debug(logText)
        
            #close files, delete variables, etc for memory management
            dictAnalysis.clear()
            reader.clear()
            del index
            del sims
            del originalId
            del originalContent
            del reader
            gc.collect()
            elapsed_time = time.time() - start_time
            print elapsed_time,": done with %s on level %s from grouping %s: %s " %(category,depth,groupingType,fileName)
            return True
        except Exception as e:
            print e
            print "File %s NOT created" %(fileName)
            return False

    def returnSimilaritiesCategoryDepth(self, category, depth):
        
        """
        Prepare data for simliratiy callculation with (category, depth)
        For category, test IR measures on depth levels
        """

        ###########            CHECK IF ALL MODELS EXIST        ##########
        notAllDone = self.checkIfExists()

        ###########            GET AND PREPARE SQL DATA         ##########
        if notAllDone:

            #DATA GROUPING MODELS
            for groupingType in grouping:
                randomItems = []
                originalContent = []
                originalId = []
        
                #different data for different grouping
                randomItems = self.shevaDB.getSimilarityDocuments(category,groupingType,self.limit,depth=depth)
                originalContent, originalId = self.shevaSimilarity.prepareComparisonDocuments(randomItems)
        
                #LOOP RHTOUGH % MODELS
                for testingDataItem in testData:
                    #file names
                    path = "%s/%s/%s/" %(self.rootModelDir,groupingType,testingDataItem)
                    fileNameLevel = "%s_%s_%s" %(testingDataItem,category,depth)
                    fileNameRange =  "%s_%s_1_%s" %(testingDataItem,category,depth)
                    
                    #CHECK PATHS FOR SIM FILES 
                    simPath = "%ssim/"%(path)
                    resultsSavePathLevel = "%s%s.csv" %(simPath,fileNameLevel)
                    resultsSavePathRange = "%s%s.csv" %(simPath,fileNameRange)
            
                    #LEVEL BASED SIM FILES 
                    if not os.path.isfile(resultsSavePathLevel):
                        #print "Started with %s\t%s\t%s\t%s\t%s\t%s" %(category, depth, groupingType, limit, testingDataItem,fileName)
                        self.calculateSimilarity(path,fileNameLevel,originalContent, originalId,category,depth, groupingType)
                            #print "Done with %s\t%s\t%s\t%s\t%s\t%s" %(category, depth, groupingType, limit, testingDataItem,fileName)
                        #else:
                            #print "Done with %s\t%s\t%s\t%s\t%s\t%s: file already exists" %(category, depth, groupingType,limit, testingDataItem,fileName)
                    else: 
                        print "Done with %s\t%s\t%s\t%s\t%s\t%s: file already exists" %(category, depth, groupingType, testingDataItem,fileName)
                    
                    #RANGE BASED SIM FILES
                    if not os.path.isfile(resultsSavePathRange):
                        #print "Started with %s\t%s\t%s\t%s\t%s\t%s" %(category, depth, groupingType, limit, testingDataItem,fileNameRange)
                        self.calculateSimilarity(path,fileNameRange,originalContent,originalId,category,depth, groupingType)
                            #print "Done with %s\t%s\t%s\t%s\t%s\t%s" %(category, depth, groupingType, limit, testingDataItem,fileNameRange)
                        #else:
                            #print "Done with %s\t%s\t%s\t%s\t%s\t%s: file already exists" %(category, depth, groupingType,limit, testingDataItem,fileNameRange)
                    else: 
                        print "Done with %s\t%s\t%s\t%s\t%s\t%s: file already exists" %(category, depth, groupingType, testingDataItem,fileNameRange)
                
                del randomItems
                del originalContent
                del originalId
                gc.collect
        else:
            print "Category %s on level %s : all models exist" %(category, depth)


#run PP
def runParallelCategory():
    ppservers = ()
    
    if len(sys.argv) > 1:
        ncpus = int(sys.argv[1])
        job_server = pp.Server(ncpus, ppservers=ppservers)
    else:
        job_server = pp.Server(ppservers=ppservers)
    
    print "Starting pp with", job_server.get_ncpus(), "workers"

    start_time = time.time()
    categories =  self.shevaDB.getMainCat()
    jobs = []
   
    i = 0
    for category in categories:
        maxDebth = self.shevaDB.getCategoryDepth(category)
        for rang in maxDebth:
            jobs.append(job_server.submit(self.returnSimilaritiesCategory, (category,rang), depfuncs = (dbQuery, returnDirectoryList, removePunct, removeStopWords, getMainCat, calculateSimilarityCSV_Summary, prepareComparisonDocuments,getOriginalRowFromModel,createDir,createCSV,), modules = ("sys", "os", "glob", "itertools", "csv","gensim.corpora","gensim.models","gensim.similarities","pp", "time", "MySQLdb","nltk","re","nltk.corpus","nltk.stem","string","gc","urlparse","pickle","logging","random","operator",)))

    for job in jobs:
        i += 1
        print i
        job()

    print "Time elapsed: ", time.time() - start_time, "s"    
    job_server.print_stats()
