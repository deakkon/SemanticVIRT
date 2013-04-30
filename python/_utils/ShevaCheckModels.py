#import
import pp, gensim,sys, os, csv,time

class checkModels:
    def checkModels(self, models):
        summaryCSVPath = "modelsLengthAnalisys.csv"
    
        if not os.path.exists(summaryCSVPath):
            summaryFile  = open(summaryCSVPath, "wb")
            csvSummary = csv.writer(summaryFile, delimiter=',', quotechar='"',quoting=csv.QUOTE_ALL)
            csvSummary.writerow(("Model","numberOfDocuments"))
        else:
            summaryFile = open(summaryCSVPath,'a')
            csvSummary = csv.writer(summaryFile, delimiter=',', quotechar='"',quoting=csv.QUOTE_ALL)
    
        path = "testData/"+models+"/models/"
        onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]
        
        for modelFile in onlyfiles:
            modelFP = "testData/"+models+"/models/"+modelFile
            tfidfModel = gensim.models.TfidfModel.load(modelFP)
            if tfidfModel.num_docs == 0:
                print modelFile
                summarySTR = ["empty",modelFile,tfidfModel.num_docs] 
                csvSummary.writerow(summarySTR)
    
    def checkCorpus(self, corpusFile, path=""):
        if path != "":
            path = "test1/0.1/corpusFiles/0.1_Regional_1_6.mm"
            corpus = gensim.corpora.MmCorpus(path)
        else:
            corpusFile
        print corpus