#import
import pp, gensim,sys, os, csv,time

class checkModels:
    def checkModels(models):
    
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
            #print path, len(onlyfiles)
            #print onlyfiles
            tfidfModel = gensim.models.TfidfModel.load(modelFP)
            if tfidfModel.num_docs == 0:
                print modelFile
                summarySTR = ["empty",modelFile,tfidfModel.num_docs] 
                csvSummary.writerow(summarySTR)
    
    def checkCorpus():
        path = "test1/0.1/corpusFiles/0.1_Regional_1_6.mm"
        corpus = gensim.corpora.MmCorpus(path)
        print corpus
    
    def checkModelsParallel():
        """
        Run comparison on n processors
        Check models for number of documents to see if there are any with 0 documents
        """
        # tuple of all parallel python servers to connect with
        ppservers = ()
        #ppservers = ("10.0.0.1",)
        
        if len(sys.argv) > 1:
            ncpus = int(sys.argv[1])
            # Creates jobserver with ncpus workers
            job_server = pp.Server(ncpus, ppservers=ppservers)
        else:
            # Creates jobserver with automatically detected number of workers
            job_server = pp.Server(ppservers=ppservers)
        
        print "Starting pp with", job_server.get_ncpus(), "workers"
        start_time = time.time()
        
        # The following submits a job for each category
        inputs = ['0.1','0.25', '0.5', '0.75', '1.0']
        #inputs =("Arts",)
        
        jobs = []
        
        for index in inputs:
            #print index
            jobs.append(job_server.submit(checkModels, (index,), depfuncs = (), modules = ("pp", "gensim","sys", "os", "csv","time",)))    
        for job in jobs:
            result = job()
            if result:
                break
        #prints
        job_server.print_stats()
        print "Time elapsed: ", time.time() - start_time, "s"

    
    
#main UI
def main():
    """
    Functions:
            1. checkModels()
            2. checkModelsParallel()
            2. checkCorpus()
            Anything else to stop
     """
    print main.__doc__

    var = raw_input("Choose function: ")
        
    if var == "1":
        print checkModels.__doc__
        checkModels()    
    elif var == "2":
        print checkModelsParallel.__doc__
        checkModelsParallel()
    elif var == "3":
        checkCorpus.__doc__
        checkCorpus()
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        
if __name__ == '__main__':    
    main()