import sys, os, glob, itertools, csv, pp, time, gensim.corpora, gensim.models, gensim.similarities, MySQLdb, nltk, string, gc, urlparse, resource, pickle, logging, random, operator
from pickle import TRUE
logging.basicConfig(filename='similarity.log',level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

#stdout
"""myFile= open( "memAnalyzer.txt", "w", 0) 
sys.stdout= myFile"""

def dbQuery(sql):
    
    #connect
    try:
        gc.collect()
        con = MySQLdb.connect(host="localhost", user="root", passwd="root", db="dmoz")
        con.autocommit(True)
    except MySQLdb.Error, e:
        print "Error dbConnect %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    
    #execute
    try:
        cur = con.cursor()
        cur.execute(sql) 
        numrows = int(cur.rowcount)
        if numrows == 1:
            resultRows =  [cur.fetchone()]
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
        print "Erroneous query: ",sql
        sys.exit(1)

def getMaxDebth(category,subcategory):
    #get root categories to be used
    sqlMainCategories = 'select max(categoryDepth) from dmoz_combined_level2 where mainCategory = "%s" and subCategory = "%s"' %(category,subcategory)
    mainCatRS = dbQuery(sqlMainCategories)
    mainCat = tuple([x[0] for x in mainCatRS])
    return mainCat

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
    #print "Remove punct ",type(text),"    ",text
    
    if type(text) is str:
        sentence = re.compile('\w+').findall(text)
    elif type(text) is list:
        sentence = text
    else:
        sys.exit("Error with data types. removePunct. textPrepareFunctions")
        
    #list of names
    male_names = nltk.corpus.names.words('male.txt')
    male_names = [name.lower() for name in male_names]    
    female_names = nltk.corpus.names.words('female.txt')
    female_names = [name.lower() for name in female_names]        
        
    #letter of the alphabet
    allTheLetters = [x for x in string.lowercase]

    #if returnType == 1:   
    sentence = [x.lower() for x in sentence]   
    #sentence = removeNames(sentence)
    sentence = [item for item in sentence if item not in allTheLetters]
    sentence = [item for item in sentence if not item.isdigit()]   
    sentence = [item for item in sentence if (item not in male_names and item not in female_names)]
    sentence = [item for item in sentence if not urlparse.urlparse(item).scheme]
    #print "punct ",sentence
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
    content = []
    
    #str to list
    if type(text) is str:
        text = text.split()        
        text = [x.lower() for x in text]        
    
    #choice of stopwords
    if mode == 1:
        stopwords = nltk.corpus.stopwords.words('english')
    elif mode == 2:
        stopwordsFileOpen = open('stopWords.txt','r')
        stopwordsFile = [i.strip() for i in stopwordsFileOpen.readlines()]
    else:
        sys.exit("False flag -> second parameter must be \n 1, if you want to use nltk based set of stopwrods \n 2, if you want to use file based set of stopwords \n")        

    content = removePunct(text)
    content = [w for w in content if w.lower() not in stopwords]
    content = [ps.stem(i) for i in content]
    return content

def getMainCat():
    """
    Returns main categories from ODP; input for PP pipeline
    """
    sqlMainCategories = "select distinct(Title) from dmoz_categories where dmoz_categories.categoryDepth = 1 and dmoz_categories.filterOut = 0"
    mainCatRS = dbQuery(sqlMainCategories)
    mainCat = tuple([x[0] for x in mainCatRS])
    return mainCat

def getSubCat(category):
    #get sub_categories to be used
    sqlMainCategories = "select distinct(subCategory) from dmoz_combined_level2 where mainCategory = '%s' and subCategory is not null" %(category)
    mainCatRS = dbQuery(sqlMainCategories)
    mainCat = tuple([x[0] for x in mainCatRS])
    return mainCat

def returnDirectoryList(path):
    directories = []
    
    for files in os.listdir(path): 
        if os.path.isdir(os.path.join(path,files)):
            #print "Directory : ",files
            directories.append(files)
    return directories

def prepareComparisonDocuments(sqlQuery):
    """
    Input: 
        sqlQuery to be executed, first parameter being textual data to convert to BoW
        
    Output parameters:
        BoW representation of documents returned from sqlQuery, list of lists
    """
    #variables
    originalID = []
    bowReturn = []    
    
    #check sqlQuery
    if sqlQuery == "":
        sys.exit("No query mate. Function prepareComparisonDocuments")
    elif type(sqlQuery) is str:
        sqlQueryResults = dbQuery(sqlQuery)
    elif type(sqlQuery) is tuple or type(sqlQuery) is list:
        sqlQueryResults = sqlQuery
    else:
        print type(sqlQuery)
        print "yaba daba doo calculateSimilarity.prepareComparisonDocuments() "
        sys.exit(1)

    #prepare BoW
    for row in sqlQueryResults:
        #print "Originalni zapis: ",row[0]
        bowReturn.append(removeStopWords(row[0]))
        originalID.append(row[1])
    #print type(bowReturn)
    gc.collect()
    return (bowReturn,originalID)
    
def getOriginalRowFromModel(modelRow, modelDocument):
    """
    Return document catid stored at modelRow row model file 
    """
    #variables
    originalRow = "Empty"
    #open csv
    f = open(modelDocument, "rb") # don't forget the 'b'!
    reader = csv.reader(f)

    #default
    for row in reader:
        #print row[0]
        if row[0] == str(modelRow):
            originalRow = row[1]
            f.close()
            return originalRow
    f.close()
        
def createDir(checkPath):
    if not os.path.isdir(checkPath):
        os.mkdir(checkPath)
        
def createCSV(savePath, content):
    with open(savePath, "wb") as the_file:
        csv.register_dialect("custom", delimiter=",", skipinitialspace=True)
        writer = csv.writer(the_file, dialect="custom")
        for item in content:
            writer.writerow(item)

#get corpus, dict, model files
def calculateSimilarityCSV_All(path,fileName,originalContent, originalId,category,depth,limit,groupingType, operationType = "3"):

    """
    Calculate similarity for originalContent against model fileName (category, depth, limit additional descriptors)
    
    operationType: DISABLED #1 -> write to database
                   1 -> write to CSV
                   2 -> filter data in dict then write in csv file
    """
    
    #check/create needed directories
    simPath = "%ssim/"%(path)
    createDir(simPath)

    operationPath = "%s%s/" % (simPath,"SummaryCSV")
    createDir(operationPath)
        
    limitPath = "%s%s/" % (operationPath,limit)
    createDir(limitPath)

    #results, originalID csv files 
    resultsSavePath = "%s%s.csv" %(limitPath,fileName)
    oidSavePath = "%s%s_original.csv" %(limitPath,fileName)

    #if not os.path.isfile(resultsSavePath):
    logText = 'Calculating similarity for %s, %s ; simFile: %s '%(category,depth,resultsSavePath)
    logging.debug(logText)
           
    #if sim file doesn't exist
    #if not os.path.isfile(resultsSavePath):
    #paths do needed files
    corpusPath = "%scorpusFiles/%s.mm" % (path,fileName)
    dictPath = "%sdict/%s.dict" % (path,fileName)
    modelPath = "%smodels/%s.tfidf_model" % (path,fileName)
    originalCATID = "%sorigCATID/%s.csv" % (path,fileName)
    #labesPath = path+"labels/"+fileName+""+".csv"

    #open needed files
    corpus = gensim.corpora.MmCorpus(corpusPath)
    dictionary = gensim.corpora.Dictionary.load(dictPath)
    tfidfModel = gensim.models.TfidfModel.load(modelPath)
    
    #create similartiy index depending on the nr of unique tokens of corpus
    if corpus.num_terms < 25000:
        index = gensim.similarities.MatrixSimilarity(tfidfModel[corpus],num_features=len(dictionary))
    else:
        tmpSim = 'tmpSim/%s_%s' %(groupingType,fileName)
        index = gensim.similarities.Similarity(tmpSim,tfidfModel[corpus],num_features=len(dictionary))
    
    #create dict, sort, filter, write to either db or csv
    dictAnalysis = {}
    originalIDList = []
    
    #csv original id from model
    f = open(originalCATID, "rb") # don't forget the 'b'!
    header = ["number of row in model","original cat id"]
    readerTemp = csv.DictReader(f,header)
    reader = {row['number of row in model']:row['original cat id'] for row in readerTemp}
    f.close()

    #csv file to store results in to
    ifile  = open(resultsSavePath, "wb")
    csvResults = csv.writer(ifile, delimiter=',', quotechar='"',quoting=csv.QUOTE_ALL)
    csvResults.writerow(("category","level","catIdEP","matrixCatID","similarity"))
    
    #csv original id from model
    f = open(originalCATID, "rb") # don't forget the 'b'!
    header = ["number of row in model","original cat id"]
    readerTemp = csv.DictReader(f,header)
    reader = {row['number of row in model']:row['original cat id'] for row in readerTemp}
    f.close()            
    
    #similarities for list of documents 
    for descriptionLevel, idLevel in  itertools.izip(originalContent,originalId):
        #print descriptionLevel, idLevel
        vec_bow = dictionary.doc2bow(descriptionLevel)
        vec_tfidf = tfidfModel[vec_bow]
        sims = index[vec_tfidf]
        sims = enumerate(sims)
        sims = sorted(sims, key=lambda item: -item[1])
        sims = [x for x in sims if x[1] > 0]
                        
        for sim in sims:
                writeData = []
                writeData.append(category)
                writeData.append(depth)
                writeData.append(idLevel)
                writeData.append(reader[str(sim[0])])
                writeData.append(sim[1])
                csvResults.writerow(writeData)
                #print writeData

        f = open(oidSavePath, 'wb')
        f.write("O_ID\n")
        for item in originalId:
            f.write("%s\n" % item)
        f.close()
    ifile.close()
        
def calculateSimilarityDatabase(path,fileName,originalContent, originalId,category,depth,limit,groupingType):

    """
    DEPRECATED: WRITE TO DATABASE
    Calculate similarity for originalContent against model fileName (category, depth, limit additional descriptors)
    """
    logText = 'Calculating similarity for %s, %s ; simFile: %s '%(category,depth,resultsSavePath)
    logging.debug(logText)
           
    #if sim file doesn't exist
    #if not os.path.isfile(resultsSavePath):
    #paths do needed files
    corpusPath = "%scorpusFiles/%s.mm" % (path,fileName)
    dictPath = "%sdict/%s.dict" % (path,fileName)
    modelPath = "%smodels/%s.tfidf_model" % (path,fileName)
    originalCATID = "%sorigCATID/%s.csv" % (path,fileName)
    #labesPath = path+"labels/"+fileName+""+".csv"

    #open needed files
    corpus = gensim.corpora.MmCorpus(corpusPath)
    dictionary = gensim.corpora.Dictionary.load(dictPath)
    tfidfModel = gensim.models.TfidfModel.load(modelPath)
    
    #create similartiy index depending on the nr of unique tokens of corpus
    if corpus.num_terms < 25000:
        index = gensim.similarities.MatrixSimilarity(tfidfModel[corpus],num_features=len(dictionary))
    else:
        tmpSim = 'tmpSim/%s_%s' %(groupingType,fileName)
        index = gensim.similarities.Similarity(tmpSim,tfidfModel[corpus],num_features=len(dictionary))
    
    #create dict, sort, filter, write to either db or csv
    dictAnalysis = {}
    originalIDList = []
    
    #csv original id from model
    f = open(originalCATID, "rb") # don't forget the 'b'!
    header = ["number of row in model","original cat id"]
    readerTemp = csv.DictReader(f,header)
    reader = {row['number of row in model']:row['original cat id'] for row in readerTemp}
    f.close()    

    #write to db
    print "blas"
    sys.exit("This option is not available. Please restart script.")

    #similarities for list of documents
    for descriptionLevel, idLevel in  itertools.izip(originalContent,originalId):
        #print descriptionLevel, idLevel
        vec_bow = dictionary.doc2bow(descriptionLevel)
        vec_tfidf = tfidfModel[vec_bow]
        sims = index[vec_tfidf]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])            
        for sim in sims:
            if float(sim[1]) != 0.0:
                matrixCatID = getOriginalRowFromModel(sim[0],originalCATID)
                #print type(sim[0]),sim[0],"    ",sim[1],"    ",matrixCatID,"     ",originalCATID
                sqlInsert = "INSERT INTO dmoz_comparisonResults (comparisonModel, category,level,catidEP,matrixID,similarity) VALUES ('"+str(fileName)+"','"+str(category)+"','"+str(depth)+"','"+str(idLevel)+"','"+str(matrixCatID)+"','"+str(sim[1])+"')"

#@profile
def calculateSimilarityCSV_Summary(path,fileName,originalContent, originalId,category,depth,limit,groupingType):
    """
    Calculate similarity for originalContent against model fileName (category, depth, limit additional descriptors)
    WRITE DATA TO SINGLE CSV FILE, AFTER APPLYING SUMMARIZATION
    3 FILES AS OUTPUT: 
        1) SUMMARY CSV FILE
        2) ORIGINALID FILE
        3) CSV FILE WITH RELATIVE VALUES FOR ALL ORIGINALID'S
    """
    try:
        start_time = time.time()
        #print start_time,": Started with %s on level %s in grouping %s: %s " %(category,depth,groupingType,fileName)

        #check/create needed directories
        simPath = "%ssim/"%(path)
        createDir(simPath)
    
        operationPath = "%s%s/" % (simPath,"SummaryCSV")
        createDir(operationPath)
            
        limitPath = "%s%s/" % (operationPath,limit)
        createDir(limitPath)
    
        #results, originalID csv files 
        resultsSavePath = "%s%s.csv" %(limitPath,fileName)
        oidSavePath = "%s%s_original.csv" %(limitPath,fileName)
        oidSavePathRelative = "%s%s_relative.csv" %(limitPath,fileName)
               
        #if not os.path.isfile(resultsSavePath):
        logText = 'Calculating similarity for %s, %s ; simFile: %s '%(category,depth,resultsSavePath)
        logging.debug(logText)
        
        #if sim file doesn't exist
        #if not os.path.isfile(resultsSavePath):
        #paths do needed files
    

        corpusPath = "%scorpusFiles/%s.mm" % (path,fileName)
        dictPath = "%sdict/%s.dict" % (path,fileName)
        modelPath = "%smodels/%s.tfidf_model" % (path,fileName)
        originalCATID = "%sorigCATID/%s.csv" % (path,fileName)
        #labesPath = path+"labels/"+fileName+""+".csv"
    
        #open needed files
        corpus = gensim.corpora.MmCorpus(corpusPath)
        dictionary = gensim.corpora.Dictionary.load(dictPath)
        tfidfModel = gensim.models.TfidfModel.load(modelPath)
        
        #create similartiy index depending on the nr of unique tokens of corpus
        if corpus.num_terms < 25000:
            index = gensim.similarities.MatrixSimilarity(tfidfModel[corpus],num_features=len(dictionary))
        else:
            tmpSim = 'tmpSim/%s_%s' %(groupingType,fileName)
            index = gensim.similarities.Similarity(tmpSim,tfidfModel[corpus],num_features=len(dictionary))
        
        #create dict, sort, filter, write to either db or csv
        dictAnalysis = {}
        dictRelative = []
        originalIDList = []
        
        #csv original id from model
        f = open(originalCATID, "rb") # don't forget the 'b'!
        header = ["number of row in model","original cat id"]
        readerTemp = csv.DictReader(f,header)
        reader = {row['number of row in model']:row['original cat id'] for row in readerTemp}
        f.close()
    
        #print "OC:\t",len(originalContent),originalContent 
        #print "OID:\t",len(originalId),originalId
        
        #similarities for list of documents
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
            sims = enumerate(sims)
            sims = [x for x in sims if x[1] > 0]
            #print "Sims:\t",len(sims),"\t",sims
            
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
    
                #if returned original value
                #print type(originalID_item), type(idLevel)
                if originalID_item == str(idLevel):
                    #print "found id level:\t", "\t",originalID_item,"\t",idLevel
                    simFound += sim[1]
                    
                #print idLevel, sim[0] , originalID_item, simFound
            #relative: if idLevel returned as similar from model calculate relative sim values
            #print type(simFound),"\t", simFound,"\t", type(sumTemp),"\t",sumTemp
            
            if sumTemp != 0:
                relativeSum = simFound/sumTemp
                dictRelative.append((idLevel,relativeSum))
            else:
                dictRelative.append((idLevel,0))
    
        #sort dictionary by sum value and write to CSV
        dictAnalysisValues = sorted(dictAnalysis.values(),key=lambda k: k['nrOcc'], reverse=True)
        keys = ['category', 'depth','idLevel','ocID','sim','nrOcc']
        f = open(resultsSavePath, 'wb')
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writer.writerow(keys)
        dict_writer.writerows(dictAnalysisValues)
        f.close()
        
        #create relative summary files
        #createCSV(oidSavePathRelative, dictRelative)
        with open(oidSavePathRelative, "wb") as the_file:
            csv.register_dialect("custom", delimiter=",", skipinitialspace=True)
            writer = csv.writer(the_file, dialect="custom")
            for item in dictRelative:
                writer.writerow(item)    
    
        #write original id's
        myfile = open(oidSavePath, 'wb')
        wr = csv.writer(myfile, delimiter=",", quoting=csv.QUOTE_ALL)
        wr.writerow(originalId)
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
    except:
        print "File %s NOT created" %(fileName)
        return False


#@profile
def returnSimilaritiesCategory(category, subcategory, depth):
    """
    COMPARE WITH ALL GROUPING MODELS
    Input:\n 
        category -> BoW representation of document for similarity comparison
        compareTo -> 1: level based comparison (default)
                     2: range based comparison
                     3: both comparisons
        limit ->    Nr. of row to return from database
    """

    #elements from query, depending on groupingType
    testData = ['0.1', '0.25', '0.5', '0.75', '1.0']
    #grouping = ['CATID','FATHERID','GENERAL']
    grouping = ['CATID']
    limits = [10,100,1000]

    #testing data
    #grouping = ["FATHERID"]
    
    ###########            CHECK IF ALL MODELS EXIST        ##########
    #LOOP RHTOUGH % MODELS
    notAllDone = False
    for limit in limits: 
        for groupingType in grouping:
            for testingDataItem in testData:
                path = "testData2/%s/%s/%s/" %(groupingType,testingDataItem,category)
                fileName = "%s_%s_%s" %(testingDataItem,subcategory,depth)
                fileNameRange =  "%s_%s_1_%s" %(testingDataItem,subcategory,depth)
                
                #CHECK PATHS FOR SIM FILES 
                simPath = "%ssim/"%(path)
                operationPath = "%s%s/" % (simPath,"SummaryCSV")
                limitPath = "%s%s/" % (operationPath,limit)
                resultsSavePathLevel = "%s%s.csv" %(limitPath,fileName)
                resultsSavePathRange = "%s%s.csv" %(limitPath,fileNameRange)    
                
                if not os.path.isfile(resultsSavePathLevel):
                    notAllDone = True
                    
                if not os.path.isfile(resultsSavePathRange):
                    notAllDone = True

    ###########            GET AND PREPARE SQL DATA         ##########
    if notAllDone:
        sqlRandomResults = []
        #sqlRandom = "SELECT Description, u2.catid, fatherid from (select catid, fatherid from dmoz_categories where mainCategory ="+category+" and categoryDepth = '"+str(depth)+"' and filterOut = '0') u1 INNER JOIN (select catid, Description from dmoz_externalpages where filterOut = '0') u2 ON u2.catid = u1.catid"
        sqlRandom = "SELECT Description, catid, fatherid from dmoz_combined_level2 where mainCategory = '%s' and subCategory = '%s' and categoryDepth = %s" %(category,subcategory,depth)
        sqlResults = dbQuery(sqlRandom)
          
        if sqlResults == 0:
            sys.exit("returnSimilaritiesCategory.sqlResults is 0.")
            
        #print type(len(sqlResults))
        for limit in limits: 
            if len(sqlResults) > int(limit):
                print len(sqlResults), "Greater then %s" %(limit)
                indices = random.sample(xrange(len(sqlResults)), int(limit))
                #print type(indices), indices
                sqlRandomResults=[sqlResults[i] for i in indices]
                #print sqlRandomResults
            else:
                print len(sqlResults), "Not greateer then %s" %(limit)
                sqlRandomResults = sqlResults
    
            #DATA GROUPING MODELS
            for groupingType in grouping:
                randomItems = []
                originalContent = []
                originalId = []        
        
                #different data for different grouping
                if groupingType != "FATHERID":
                    randomItems = [operator.itemgetter(0,1)(i) for i in sqlRandomResults]
                else:
                    randomItems = [operator.itemgetter(0,2)(i) for i in sqlRandomResults]
                    
                originalContent, originalId = prepareComparisonDocuments(randomItems)
        
                #LOOP RHTOUGH % MODELS
                for testingDataItem in testData:
                    #print category, depth, groupingType, testingDataItem,len(originalContent), len(originalId)
                    #file names
                    path = "testData2/%s/%s/%s/" %(groupingType,testingDataItem,category)
                    fileName = "%s_%s_%s" %(testingDataItem,subcategory,depth)
                    fileNameRange =  "%s_%s_1_%s" %(testingDataItem,subcategory,depth)
                    
                    #CHECK PATHS FOR SIM FILES 
                    simPath = "%ssim/"%(path)    
                    operationPath = "%s%s/" % (simPath,"SummaryCSV")
                    limitPath = "%s%s/" % (operationPath,limit)
                    resultsSavePathLevel = "%s%s.csv" %(limitPath,fileName)
                    resultsSavePathRange = "%s%s.csv" %(limitPath,fileNameRange)
            
                    #LEVEL BASED SIM FILES 
                    if not os.path.isfile(resultsSavePathLevel):
                        print "Started with %s\t%s\t%i\t%s\t%s\t%s\t%s" %(category, subcategory, depth, groupingType, limit, testingDataItem,fileName)
                        if calculateSimilarityCSV_Summary(path,fileName,originalContent, originalId,subcategory,depth,limit, groupingType):
                            print "Done with %s\t%s\t%i\t%s\t%s\t%s\t%s" %(category, subcategory, depth, groupingType, limit, testingDataItem,fileName)
                        else:
                            print "Done with  %s\t%s\t%i\t%s\t%s\t%s\t%s: file already exists" %(category, subcategory, depth, groupingType, limit, testingDataItem,fileName)
                    else: 
                        print "Done with  %s\t%s\t%i\t%s\t%s\t%s\t%s: file already exists" %(category, subcategory, depth, groupingType, limit, testingDataItem,fileName)
                    
                    #RANGE BASED SIM FILES
                    if not os.path.isfile(resultsSavePathRange):
                        print "Started with  %s\t%s\t%i\t%s\t%s\t%s\t%s" %(category, subcategory, depth, groupingType, limit, testingDataItem,fileNameRange)
                        if calculateSimilarityCSV_Summary(path,fileNameRange,originalContent,originalId,subcategory,depth,limit, groupingType):
                            print "Done with  %s\t%s\t%i\t%s\t%s\t%s\t%s" %(category, subcategory, depth, groupingType, limit, testingDataItem,fileNameRange)
                        else:
                            print "Done with  %s\t%s\t%i\t%s\t%s\t%s\t%s: file already exists" %(category, subcategory, depth, groupingType, limit, testingDataItem,fileNameRange)
                    else: 
                        print "Done with  %s\t%s\t%i\t%s\t%s\t%s\t%s: file already exists" %(category, subcategory, depth, groupingType, limit, testingDataItem,fileNameRange)
                
                del randomItems
                del originalContent
                del originalId
                gc.collect
    else:
        print "Category %s on level %s : all models exist" %(category, depth)


#run PP
def runParallelCategory():
    """
    Run comparison on n processors
    """
    # tuple of all parallel python servers to connect with
    #print type(sys.argv), sys.argv
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
    categories = getMainCat()
    jobs = []
   
    i = 0
    for category in categories:
            subCat = getSubCat(category)
            for subcategory in subCat:
                scMaxDebth = getMaxDebth(category,subcategory)
                maxDebth = scMaxDebth[0]
                ranger = [x for x in range(3,maxDebth+1)]
                for rang in ranger:
                    jobs.append(job_server.submit(returnSimilaritiesCategory, (category,subcategory,rang,), depfuncs = (dbQuery, returnDirectoryList, removePunct, removeStopWords, getMainCat, calculateSimilarityCSV_Summary, prepareComparisonDocuments,getOriginalRowFromModel,createDir,createCSV,getMaxDebth,getSubCat,), modules = ("sys", "os", "glob", "itertools", "csv","gensim.corpora","gensim.models","gensim.similarities","pp", "time", "MySQLdb","nltk","re","nltk.corpus","nltk.stem","string","gc","urlparse","pickle","logging","random","operator",)))

    for job in jobs:
        i += 1
        print i
        job()
        #print results

    print "Time elapsed: ", time.time() - start_time, "s"    
    job_server.print_stats()


#main UI
def main():
    """
    Functions:
            1. getMainCat()
            2. prepareComparisonDocuments(sqlQuery)
            3. getFileList(folder)
            4. getOriginalRowFromModel(modelRow, modelDocument="")
            5. returnSimilaritiesCategory("Arts",compareTo="3", limit = 10)
            6. runParallelCategory()
            Anything else to stop
     """
    print main.__doc__

    var = raw_input("Choose function: ")
        
    if var == "1":
        print getMainCat.__doc__
        getMainCat()    
    if var == "2":
        print prepareComparisonDocuments.__doc__
        var1 = raw_input("Insert SQL query")
        prepareComparisonDocuments(var1)        
    elif var == "3":
        print getFileList.__doc__
        var1 = raw_input("Folder to list data from (experimental): ")
        getFileList(var1)
    elif var == "4":
        print getOriginalRowFromModel.__doc__
        print getOriginalRowFromModel(modelRow="107", modelDocument="testData2/0.1/origCATID/0.1_News_3.csv")
    elif var == "5":
        myFile= open("memory1.txt", "w") 
        #sys.stdout= myFile
        print returnSimilaritiesCategory.__doc__
        returnSimilaritiesCategory("Arts",5)
    elif var == "6":
        print runParallelCategory.__doc__
        runParallelCategory()
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        
if __name__ == '__main__':    
    main()