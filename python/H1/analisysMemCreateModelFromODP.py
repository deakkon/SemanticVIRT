'''
Created on 9.1.2013.

@author: Jurica Seva

PhD Candidate 
Faculty of Organization and Informatics
University of Zagreb

Functions:
    1. dbQuery(sql)
    2. errorMessage(msg)
    3. removePunct(text)
    4. removeStopWords(text, mode=1)
    5. createCorpusAndVectorModel(data, dataSet, fileName ="", outputFormat=1, modelFormat=1)
    6. getCategoryLabel(categoryLabels,fileName, dataSet)
    7. getCategoryListLevel(catID, fileName, dataset)
    8. getMainCat()
    9. createData(category)
    10. runParallel()
'''
#imports
import math, sys, time, csv, os, string, pp, re, gensim, MySQLdb, nltk.corpus, nltk.stem, itertools,urlparse,gc
from MySQLdb import *
from nltk.stem import WordNetLemmatizer, PorterStemmer, LancasterStemmer

#stemmers
wnl = nltk.stem.WordNetLemmatizer()
lst = nltk.stem.LancasterStemmer()
ps = nltk.stem.PorterStemmer()

#Database stuff    
def dbQuery(sql):

    try:
        gc.collect()
        con = MySQLdb.connect(host="localhost", user="root", passwd="root", db="dmoz")
        con.autocommit(True)  
    
    except MySQLdb.Error, e:
        print "Error dbConnect %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
        
    try:
        cur = con.cursor()   
        cur.execute(sql) 
        numrows = int(cur.rowcount)
        if numrows == 1:
            resultRows = [cur.fetchone()]
        elif numrows > 1: 
            resultRows = [x for x in cur.fetchall()]
        else: 
            resultRows = 0
        
        cur.close()
        con.close()
        gc.collect()
        return resultRows
    
    except MySQLdb.Error, e:
        print "Error dbQuery %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

def errorMessage(msg):
    print msg
    sys.exit(1)

#prepare text for gensim stuff

def removePunct(text):
    """
    Input arguments: text (text to remove punctuation from), returnType (what to return; default string)
    Return types: type list (of words) if returnType = 1, string if returnType = 2 (default)
    
    Removes:
        single letters 
        numbers 
        first male/female names
        punctuation
    """
    #data preparation   
    if type(text) is str:
        sentence = re.compile('\w+').findall(text)
    elif type(text) is list:
        sentence = text
    else:
        print type(text)
        sys.exit("Error with data types. removePunct. textPrepareFunctions")
    
    #list of names
    male_names = nltk.corpus.names.words('male.txt')
    male_names = [name.lower() for name in male_names]    
    female_names = nltk.corpus.names.words('female.txt')
    female_names = [name.lower() for name in female_names]
    allTheLetters = [x for x in string.lowercase]

    #clean up
    sentence = [x.lower() for x in sentence]
    sentence = [item for item in sentence if item not in allTheLetters]
    sentence = [item for item in sentence if not item.isdigit()]   
    sentence = [item for item in sentence if (item not in male_names and item not in female_names)]
    sentence = [item for item in sentence if not urlparse.urlparse(item).scheme]
    return sentence

def removeStopWords(text, mode=1):        
    """
    Removes stop words from text, passed as variable text
    text: type list
    mode -> type of stop words list to use:
        1 = stem words from nltk.corpus.stopwords.words
        2 = stop words from file stopWords.txt (default)
        
    Output: stemmed (Porter stemmer) list of words that are not defined as stopwords, type list
    """    
    ps = nltk.stem.PorterStemmer()
    
    #print type(text),"   \t",text
    #str to list
    if type(text) is str:
        text = text.split()        
        text = [x.lower() for x in text]
    #print type(text),"   \t",text

    #variables
    content = []
    
    #choice of stopwords
    if mode == 1:
        stopwords = nltk.corpus.stopwords.words('english')
    elif mode == 2:
        stopwordsFileOpen = open('stopWords.txt','r')
        stopwordsFile = [i.strip() for i in stopwordsFileOpen.readlines()]
    else:
        sys.exit("False flag -> second parameter must be \n 1, if you want to use nltk based set of stopwrods \n 2, if you want to use file based set of stopwords \n")        

    content = removePunct(text)
    #print content
    content = [w for w in content if w.lower() not in stopwords]
    #print content
    content = [ps.stem(i) for i in content]
    #print content
    return content

#@profile
def createCorpusAndVectorModel(data, dataSet, fileName ="", outputFormat=1, modelFormat=1):
    """
    Input parameters: sqlQueryResults="", outputFormat=1, modelFormat=1, fileName =""
        1. data -> data to save to models, corpus, dictionary
        2. dataset: % model of all data; part of dirName where to save files
        3. fileName -> if "" use dummy name
        4. outputFormat definition:     1 -> MmCorpus (default)
                                        2 -> SvmLightCorpus
                                        3 -> BleiCorpus
                                        4 -> LowCorpus
        5. modelFormat:                 1 -> tfidf_model (default)
                                        2 -> lsi
                                        3 -> lda                                                                                                                            
    Output data: saved dictionary, corpus and model files of chosen format to disk, to respected directories
    """   
    path = "test1/"+str(dataSet)+"/"
    
    #create file names to save
    if fileName == "":
        sys.exit("No file name given.")
    
    #create dictionary
    dictionary = gensim.corpora.Dictionary(data)
    dictFN = path+"dict/"+fileName+".dict"
    dictionary.save(dictFN)
    
    #creating dictionary and corpus  files in different matrix formats    
    bow_documents = [dictionary.doc2bow(text) for text in data]

    #create corpora data for use in creating a vector model representation for furher use
    corpora = path+"corpusFiles/"+fileName
    if outputFormat == 1:
        saveCorpora = corpora+".mm"
        gensim.corpora.MmCorpus.serialize(saveCorpora, bow_documents)
        #print "corpus created"
    elif outputFormat == 2:
        saveCorpora = corpora+".svmlight"
        gensim.corpora.SvmLightCorpus.serialize(saveCorpora, bow_documents)
    elif outputFormat == 3:
        saveCorpora = corpora+".lda-c"
        gensim.corpora.BleiCorpus.serialize(saveCorpora, bow_documents)
    elif outputFormat == 4:
        saveCorpora = corpora+".low" 
        gensim.corpora.LowCorpus.serialize(saveCorpora, bow_documents)
    else:
        errorMessage("Something went wrong with the corpus type identificator")
        
    
    #save model to disk -> model of all documents that are going to be compared against
    model = path+"models/"+fileName
    if modelFormat == 1:
        tfidf = gensim.models.TfidfModel(bow_documents)
        saveModel = model+".tfidf_model"
        tfidf.save(saveModel)
        #print "corpus created"
    elif modelFormat == 2:
        lsi = gensim.models.LsiModel(bow_documents)
        saveModel = model+".lsi"
        lsi.save(saveModel)
    elif modelFormat == 3:
        lda = gensim.models.LdaModel(bow_documents)
        saveModel = model+".lda"
        lda.save(saveModel)
    else:
        errorMessage("createTrainingModel: Something went wrong with the type identificator")
    """
    #create and save similarity index files for comparison
    corpus = gensim.corpora.MmCorpus(saveCorpora)
    dictionary = gensim.corpora.Dictionary.load(dictFN)
    tfidfModel = gensim.models.TfidfModel.load(saveModel)
    index = gensim.similarities.MatrixSimilarity(tfidfModel[corpus], num_features=len(dictionary))
    simIndeks = path+"indeks/"+fileName+".index"
    index.save(simIndeks)
    print "simIndeks created"
    del index
    """
    gc.collect()
    return None

def getCategoryLabel(categoryLabels,fileName, dataSet):
    """
    categoryLabels -> list of labels to write to disk
    fileName -> file to save labels returned by the query
    """
    #lables array for level, for % of accesed rows
    writeLabels = []    

    #file to save data to 
    fileName = "test1/"+str(dataSet)+"/labels/"+fileName+".csv"
    ifile  = open(fileName, "wb")
    out = csv.writer(ifile, delimiter=',',quoting=csv.QUOTE_ALL)

    for row in categoryLabels:
        for i in row:            
            if i != "" or i.lower() not in string.letters.lower():
                writeLabels.append(i.lower())
    out.writerow(writeLabels)

def getCategoryListLevel(catID, fileName, dataset):
    """
    catID: original cadID while creating data
    fileName: fileName for saving
    dataset: % model of data
    """
    #create csv
    resultsSavePath = "test1/"+str(dataset)+"/origCATID/"+str(fileName)+".csv"
    summaryFile  = open(resultsSavePath, "wb")
    csvResults = csv.writer(summaryFile, delimiter=',',quoting=csv.QUOTE_ALL)
    csvResults.writerow(('number of row in model','original cat id'))

    for i in list(enumerate(catID)):
        #print i
        if str(i[1]) == "e":
            print "Es in the house:\t",i[0],"\t",i[1]
        else:
            csvResults.writerow((i[0],i[1]))
    
    summaryFile.close()
    gc.collect()
    return None

def getMainCat():
    #get root categories to be used
    sqlMainCategories = "select distinct(Title) from dmoz_categories where dmoz_categories.categoryDepth = 1 and dmoz_categories.filterOut = 0"
    mainCatRS = dbQuery(sqlMainCategories)
    mainCat = tuple([x[0] for x in mainCatRS])
    return mainCat

def createData(category):
    """
    1. get root categories to be used and iterate through main categories
    3. get max depth for individual category
    4. from 1 to max till 1 to 1
        get all catid for iterated category
        get all pages for selected categories
        call createCorpusAndVectorModel fro selected documents
    """
    #percentage of data to be used for model build
    #percentageList = [0.1, 0.25, 0.5, 0.75, 1.0]
    percentageList = [0.1]
    
    #get max debth
    sqlmaxDepth = "select max(categoryDepth) from dmoz_categories where Topic like 'Top/"+str(category)+"/%' and filterOut = 0"
    maxDebthRS = dbQuery(sqlmaxDepth)
    maxDebth = maxDebthRS[0]
    maxDebth = int(maxDebth[0])
    ranger = [x for x in range(2,maxDebth+1)]
    #print type(ranger[2])
    #print ranger

    #specific % models
    for percentageItem in percentageList:
        #(1,indeks) list variables
        dataCategoryLevelAll = []
        dataCategoryLabelAll = []
        originalCatIDAll = []
        dataCategorySingleAll = []

        #basic directory for model, based on % of data being analyzed
        path = "test1/"+str(percentageItem)+"/"
        if not os.path.isdir(path):
            os.mkdir(path)
            
        #path to dict, model, corpusFiles directory, sim, labels, origCATID directories
        pathSubDir = ["dict/","models/","corpusFiles/","labels/","origCATID/","sim/", "indeks"]
        for pathItem in pathSubDir:
            checkPath = path+pathItem
            if not os.path.isdir(checkPath):
                os.mkdir(checkPath)

        #print header for (cat,level,model)
        #print "Category    Level    PercentageModel    LevelAllRows    ModelRows    IDRows    CombinedRows    CombinedID"

        #go through all levels (2,maxDebth)
        for indeks in ranger:
            print category,"\t",percentageItem,"\t",indeks
            
            #create file names
            fileNameAll = str(percentageItem)+"_"+category+"_1_"+str(indeks)
            fileNameLevel = str(percentageItem)+"_"+category+"_"+str(indeks)
            fileNameSingleAll = str(percentageItem)+"_"+category+"_"+str(indeks)+"_single"
            
            #dynamic SQL queries
            sqlCategoryLevel = "select Description,Title,link,catid from dmoz_externalpages where filterOut = 0 and catid in (select catid from dmoz_categories where Topic like 'Top/"+category+"/%' and categoryDepth = "+str(indeks)+" and filterOut = 0)"            
            #sqlCategoryLabel = "select distinct(Title) from dmoz_categories where Topic like 'Top/"+category+"/%' and categoryDepth = "+str(indeks)+ " and filterOut = 0"
    
            #level list variables
            dataCategoryLevel = []
            dataCategoryLabel = []
            originalCatID = []
            originalFatherID = []

            ##########   ORIGINAL DESCRIPTION AND VECTORIZATION  #################
            sqlQueryResultsLevel = dbQuery(sqlCategoryLevel)
            
            if sqlQueryResultsLevel == 0:
                print category,"\t",indeks,"\t",sqlCategoryLevel
            # % of rows
            percentageLevel = int(percentageItem * int((len(sqlQueryResultsLevel))))
            
            
            # if % rows = 0 take at least one
            if percentageLevel == 0:
                percentageLevel = 1
  
            #print type(sqlQueryResultsLevel),"\t",len(sqlQueryResultsLevel),"\t", type(lrows),len(lrows),"\t"

            #prepare % of returned documents for analysis
            for row in sqlQueryResultsLevel[:percentageLevel]:
                #print type(row[0]),"\n",row[0],"\n",row
                if str(row[3]) == "e":
                    print "row je cudan:\t",row[3]
                else:
                    dataCategoryLevel.append(removeStopWords(row[0]))
                    originalCatID.append(row[3])
 

            #create corpus models
            createCorpusAndVectorModel(dataCategoryLevel,percentageItem,fileName=fileNameLevel)
            dataCategoryLevelAll.extend(dataCategoryLevel)
            createCorpusAndVectorModel(dataCategoryLevelAll, percentageItem, fileName=fileNameAll)

            #single model for all documents
            #dataCategorySingleAll.append([x for sublist in dataCategoryLevelAll for x in sublist])
            #createCorpusAndVectorModel(dataCategorySingleAll, percentageItem, fileName=fileNameSingleAll)

            ##########   ORIGINAL CATEGORIES ID   #################
            getCategoryListLevel(originalCatID,fileNameLevel,percentageItem)
            originalCatIDAll.extend(originalCatID)
            getCategoryListLevel(originalCatIDAll,fileNameAll,percentageItem)

            #print out number of documents for (cat,level,model)
            #print category,"    ",indeks,"    ",percentageItem,"    ",len(sqlQueryResultsLevel),"    ",len(dataCategoryLevel),"    ",len(originalCatID),"    ",len(dataCategoryLevelAll),"    ",len(originalCatIDAll)

            #######################    LABEL    #################
            """
            sqlQueryResultsLabel = dbQuery(sqlCategoryLabel)
            percentageLabel = int(percentageItem * len(sqlQueryResultsLabel))
            for row in sqlQueryResultsLabel[:percentageLabel]:
                    dataCategoryLabel.append(removeStopWords(row[0]))
                        
            getCategoryLabel(dataCategoryLabel,fileNameLevel,percentageItem)
            dataCategoryLabelAll.extend(dataCategoryLabel)
            getCategoryLabel(dataCategoryLabelAll,fileNameAll, percentageItem)
            """
            gc.collect()
    
    return None
            

def runParallel():
    """
    Run comparison on n processors
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
    inputs = getMainCat()
    #print inputs
    #inputs =("Arts",)
    
    jobs = []

    for index in inputs:
        #print index
        jobs.append(job_server.submit(createData, (index,), depfuncs = (dbQuery,createCorpusAndVectorModel,getCategoryLabel,removeStopWords,removePunct,dbQuery,errorMessage,getCategoryListLevel,), modules = ("math", "sys", "time", "csv", "os", "string", "pp","gensim","MySQLdb","gensim.corpora","gensim.models","re","nltk.corpus","nltk.stem","itertools","urlparse","gc",)))
    
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
        1. createData(category)
        2. runParallel()
        3. getMainCat()
            Anything else to stop
     """
    print main.__doc__

    var = raw_input("Choose function: ")
        
    if var == "1":
        myFile= open( "createMemoryAnalyzer.txt", "w") 
        #sys.stdout= myFile
        print createData.__doc__
        createData("Regional")
    elif var == "2":
        print runParallel.__doc__
        runParallel()
    elif var == "3":
        getMainCat.__doc__
        print getMainCat()
    else:
        print "Hm, ", var," not supported as an option"
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':    
    main()