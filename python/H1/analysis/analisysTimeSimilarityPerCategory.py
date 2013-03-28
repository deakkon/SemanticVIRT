'''
Created on 8.1.2013.

@author: Jurica Seva

PhD Candidate 
Faculty of Organization and Informatics
University of Zagreb

Functions:
1. getMainCat()
2. prepareComparisonDocuments(sqlQuery)
3. getFileList(folder)
4. returnSimilarities(category, compareTo="1")
5. runParallel()

'''
#imports
import sys, os, glob, itertools, csv, pp, time, gensim.corpora, gensim.models, gensim.similarities, MySQLdb, nltk, string, gc, urlparse, resource, caulk
caulk.install()

#stdout
"""myFile= open( "memAnalyzer.txt", "w", 0) 
sys.stdout= myFile"""

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

def errorMessage(msg):
    print msg
    return

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
        
    #print sqlQueryResults
        
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
    #reader = csv.DictReader(f, header)
    #header = reader.next()
    
    #default
    for row in reader:
        #print row[0]
        if row[0] == str(modelRow):
            originalRow = row[1]
            f.close()
            return originalRow
    f.close()

#get corpus, dict, model files
@profile
def calculateSimilarity(path,fileName,originalContent, originalId,category,depth,limit,operationType = "3"):
    """
    operationType: 1 -> write to database
                   2 -> write to CSV 
                   3 -> filter data in dict then write in csv file
    path:
    fileName:
    originalContent:
    originalId:
    category:
    depth    
    """  
    #resultsSavePath = path+"sim/"+fileName+".csv"
    resultsSavePath = "%ssim/%s.csv" %(path,fileName)
           
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
    #print "ucitani modeli i ostalo"
    
    #TO DO: if sim file saved on disk read from disk else create new
    index = gensim.similarities.MatrixSimilarity(tfidfModel[corpus],num_features=len(dictionary))
    #print "izracunat sim index"
    
    #write to db
    if operationType == "1":
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
                    #print sqlInsert
                    #dbQueryInsert(sqlInsert)

    #write to file
    elif operationType == "2":
        #csv file to store results in to
        ifile  = open(resultsSavePath, "wb")
        csvResults = csv.writer(ifile, delimiter=',', quotechar='"',quoting=csv.QUOTE_ALL)
        csvResults.writerow(("category","level","catIdEP","matrixCatID","similarity"))
        
        #similarities for list of documents 
        for descriptionLevel, idLevel in  itertools.izip(originalContent,originalId):
            #print descriptionLevel, idLevel
            vec_bow = dictionary.doc2bow(descriptionLevel)
            vec_tfidf = tfidfModel[vec_bow]
            sims = index[vec_tfidf]
            sims = sorted(enumerate(sims), key=lambda item: -item[1])              
            for sim in sims:
                if float(sim[1]) != 0.0:
                    writeData = []
                    writeData.append(category)
                    writeData.append(depth)
                    writeData.append(idLevel)
                    writeData.append(getOriginalRowFromModel(sim[0],originalCATID))
                    writeData.append(sim[1])
                    csvResults.writerow(writeData)
                    #print writeData
    
    #create dict, sort, filter, write to either db or csv
    elif operationType == "3":

        #define dictionary
        dictAnalysis = {}
        
        #csv original id from model
        #print originalCATID
        f = open(originalCATID, "rb") # don't forget the 'b'!
        header = ["number of row in model","original cat id"]
        readerTemp = csv.DictReader(f,header)
        reader = {row['number of row in model']:row['original cat id'] for row in readerTemp}
        f.close()

        #similarities for list of documents
        for descriptionLevel, idLevel in  itertools.izip(originalContent,originalId):
            vec_bow = dictionary.doc2bow(descriptionLevel)
            vec_tfidf = tfidfModel[vec_bow]
            #sims = []
            sims = index[vec_tfidf]
            sims = enumerate(sims)
            sims = [x for x in sims if x[1] > 0]
            #sims = sorted(enumerate(index[vec_tfidf]), key=lambda item: -item[1])
            #sims = [x for x in enumerate(index[vec_tfidf]) if x[1] > 0]
            for sim in sims:
                if sim[0] in dictAnalysis:
                    dictAnalysis[sim[0]]['nrOcc'] += 1
                    dictAnalysis[sim[0]]['sim']+=sim[1]
                else:
                    originalIDtTem=reader[str(sim[0])]
                    dictAnalysis[sim[0]] = {'category': category, 'depth': depth, 'idLevel': idLevel, 'ocID': int(originalIDtTem), 'sim':sim[1], 'nrOcc': 1}

        #sort dictionary by sum value and write to CSV
        dictAnalysisValues = sorted(dictAnalysis.values(),key=lambda k: k['sim'], reverse=True)
        keys = ['category', 'depth','idLevel','ocID','sim','nrOcc']
        f = open(resultsSavePath, 'wb')
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writer.writerow(keys)
        dict_writer.writerows(dictAnalysisValues)
        f.close()
        
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
        #print category,"\t",depth,"\t",fileName,"\t",tfidfModel.num_docs,"\t",len(dictAnalysis.keys()),"\t",len(originalContent)
        
        #close files, delete variables, etc for memory management
        dictAnalysis.clear()
        reader.clear()
        return None
    else:
        sys.exit("Unknown flag calculateSimilarity.operationType")
    """   
    else:
        print "Similartiy file "+resultsSavePath+" already exists."
    """

#return similarities based on a category comparison; get random documents from category, scattered through levels.
@profile
def returnSimilaritiesCategory(category, compareTo="3", limit = "100"):
    """
    Input:\n 
        category -> BoW representation of document for similarity comparison
        compareTo -> 1: level based comparison (default)
                     2: range based comparison
                     3: both comparisons
        limit ->    Nr. of row to return from database
    """
     
    #get cat debth
    sqlmaxDepth = "select max(categoryDepth) from dmoz_categories where Topic like 'Top/"+str(category)+"/%' and filterOut = 0"
    maxDebthRS = dbQuery(sqlmaxDepth)
    maxDebth = maxDebthRS[0]
    #print maxDebthRS,"\t",maxDebth,"\t",type(maxDebth)
    maxDebth = maxDebth[0]
    #maxDebth = int(maxDebth[0])
    ranger = [x for x in range(2,maxDebth+1)]
    #ranger = [4]
    
    #singular comparison, get directory listing where models are stored
    #testData = ['0.1','0.25', '0.5', '0.75', '1.0']
    testData = ['0.1']

    #for model 
    for testingDataItem in testData:
        #print "Model:\t ispis1\t",testingDataItem
        #get random documents from database for cat; get catid and all files from dmoz_externalpages for each catid
        for depth in ranger:
            #print category,"\t",depth
            #print "Model:\tispis2\t",testingDataItem
            #print "Model:\tispis2\t",testingDataItem
            
            #range specific variables
            originalContent = []
            originalId = []

            #queries, get random documents limit
            sqlRandom = "SELECT ep.Description, ep.catid FROM dmoz_externalpages ep LEFT JOIN dmoz_categories c ON ep.catid = c.catid where Topic like 'Top/"+str(category)+"/%' and categoryDepth = "+str(depth)+" and c.filterOut = 0 and ep.filterOut = 0 limit "+limit
            sqlRandomResults = dbQuery(sqlRandom)
            
            """
            if len(sqlRandomResults)>limit:
                indices = random.sample(range(len(sqlRandomResults)), limit)
                sqlRandomResults=[sqlRandomResults[i] for i in sorted(indices)]
            """
            
            #print "sql query: ",sqlRandom
            originalContent, originalId = prepareComparisonDocuments(sqlRandomResults)
            #print "Model:\tispis3\t",sqlRandom

            #dynamic path, data to be compared to
            #path = "testData/"+str(testingDataItem)+"/"
            path = "test2/"+str(testingDataItem)+"/"
            fileName = testingDataItem+"_"+category+"_"+str(depth)
            fileNameRange =  testingDataItem+"_"+category+"_1_"+str(depth)
    
            #load files from disk needed for similarity indexing
            if compareTo == "1":
                calculateSimilarity(path,fileName,originalContent, originalId,category,depth,limit)
            elif compareTo == "2":
                calculateSimilarity(path,fileNameRange,originalContent,originalId,category,depth,limit)
            elif compareTo == "3":
                calculateSimilarity(path,fileName,originalContent, originalId,category,depth,limit)
                calculateSimilarity(path,fileNameRange,originalContent,originalId,category,depth,limit)
            else:
                sys.exit("Something went wrong with similarity calculation. ")
            #force garbage collect
    gc.collect()
    return
            
#run PP
def runParallelCategory():
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
    #inputs =("Arts",)
    
    jobs = []
    
    for index in inputs:
        #print index
        jobs.append(job_server.submit(returnSimilaritiesCategory, (index,), depfuncs = (dbQuery, errorMessage, returnDirectoryList, removePunct, removeStopWords, getMainCat, calculateSimilarity, prepareComparisonDocuments,getOriginalRowFromModel,), modules = ("sys", "os", "glob", "itertools", "csv","gensim.corpora","gensim.models","gensim.similarities","pp", "time", "MySQLdb","nltk","re","nltk.corpus","nltk.stem","string","gc","urlparse","caulk",)))    
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
            1. getMainCat()
            2. prepareComparisonDocuments(sqlQuery)
            3. getFileList(folder)
            4. getOriginalRowFromModel(modelRow, modelDocument="")
            5. returnSimilaritiesCategory("News",compareTo="3", limit = "100")
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
        print getOriginalRowFromModel(modelRow="107", modelDocument="testData/test/origCATID/0.1_News_3.csv")
    elif var == "5":
        myFile= open( "timeAnalyzer.txt", "w") 
        sys.stdout= myFile
        print returnSimilaritiesCategory.__doc__
        returnSimilaritiesCategory("Regional",compareTo="3", limit = "100")
    elif var == "6":
        print runParallelCategory.__doc__
        runParallelCategory()             
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        
if __name__ == '__main__':    
    main()
    