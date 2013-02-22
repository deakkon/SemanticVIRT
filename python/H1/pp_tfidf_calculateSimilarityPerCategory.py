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
import sys, os, glob, itertools, csv, pp, time, gensim.corpora, gensim.models, gensim.similarities, MySQLdb, nltk, string, gc


#stdout
"""myFile= open( "memAnalyzer.txt", "w", 0) 
sys.stdout= myFile"""

def dbQuery(sql):

    try:
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
            resultRows = cur.fetchone()
        elif numrows > 1: 
            resultRows = cur.fetchall()
        else: 
            resultRows = 0        
        return resultRows    
        cur.close()
        con.close()
    
    except MySQLdb.Error, e:
        print "Error dbQuery %d: %s" % (e.args[0],e.args[1])
        print sql
        sys.exit(1)

def errorMessage(msg):
    print msg
    sys.exit(1)

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
    elif type(sqlQuery) is tuple:
        sqlQueryResults = sqlQuery
    else:
        print type(sqlQuery)
        print "yaba daba doo calculateSimilarity.prepareComparisonDocuments() "
        sys.exit(1)
        
    #prepare BoW
    for row in sqlQueryResults:
        #print "Originalni zapis: ",row[0]
        if type(row) is not long:
            bowReturn.append(removeStopWords(row[0]))
            originalID.append(row[1])
    #print type(bowReturn)
    return (bowReturn,originalID)

    #try to manage memory
    del sqlQueryResults, originalID, bowReturn
    gc.collect()
    
def getOriginalRowFromModel(modelRow, modelDocument=""):  
    #variables
    find = False
    
    #find original cat id at position modelRow
    with open(modelDocument, "rb" ) as theFile:
        reader = csv.DictReader( theFile )
        while find is False:
            for line in reader:
                if line['number of row in model'] == str(modelRow):
                    #print line
                    #print line['number of row in model']
                    #print line['original cat id']
                    #print type(line['original cat id'])
                    find = True
                    return line['original cat id']
                    
                 
            
        
#get corpus, dict, model files
#@profile
def calculateSimilarity(path,fileName,originalContent, originalId,category,depth,operationType = "3"):
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
    #define dictionary
    #if operationType == "3":
    dictAnalysis = {}
    #print len(dictAnalisys)
    
    #paths do needed files
    corpusPath = path+"corpusFiles/"+fileName+""+".mm"
    dictPath = path+"dict/"+fileName+".dict"
    modelPath = path+"models/"+fileName+""+".tfidf_model"
    labesPath = path+"labels/"+fileName+""+".csv"
    resultsSavePath = path+"sim/"+fileName+".csv"
    originalCATID = path+"origCATID/"+fileName+".csv"
    """
    #print paths
    print corpusPath
    print dictPath
    print modelPath
    print labesPath
    print resultsSavePath
    print originalCATID
    """    
    
    #open needed files
    corpus = gensim.corpora.MmCorpus(corpusPath)
    dictionary = gensim.corpora.Dictionary.load(dictPath)
    tfidfModel = gensim.models.tfidfmodel.TfidfModel.load(modelPath)
    index = gensim.similarities.MatrixSimilarity(tfidfModel[corpus],num_features=len(dictionary))
    
    #create save csv if needed
    #save csv file
    #define dictionary
    if operationType == "1":    
        ifile  = open(resultsSavePath, "w")
        csvResults = csv.writer(ifile, delimiter=',', quotechar='"',quoting=csv.QUOTE_ALL)
        csvResults.writerow(("category","level","catIdEP","matrixCatID","similarity"))
    
    #CONTENT PART; CALCULATE SIMILARTIY BASED ON TFIDF, RETURN TOP(n) DOCUMENTS BY SIMILARITY
    for descriptionLevel, idLevel in  itertools.izip(originalContent,originalId):
        vec_bow = dictionary.doc2bow(descriptionLevel)
        vec_tfidf = tfidfModel[vec_bow]
        sims = index[vec_tfidf]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        #WRITE SIMLARITY RESULTS TO CSV
        #for sim in sims[:sample]:
        if operationType == "1":
            #if similarity file doesn't exist, to speed up the process; delete if afterwards
            #if not os.path.isfile(resultsSavePath):                
            for sim in sims:
                if sim[1] != 0.0:
                    sqlInsert = "INSERT INTO dmoz_comparisonResults (comparisonModel, category,level,catidEP,matrixID,similarity) VALUES ('"+str(fileName)+"','"+str(category)+"','"+str(depth)+"','"+str(idLevel)+"','"+str(getOriginalRowFromModel(sim[0],originalCATID))+"','"+str(sim[1])+"')"
                    #print sqlInsert
                    dbQuery(sqlInsert)
        elif operationType == "2":
            for sim in sims:
                if sim[1] != 0.0:
                    writeData = []
                    writeData.append(category)
                    writeData.append(depth)
                    writeData.append(idLevel)
                    writeData.append(getOriginalRowFromModel(sim[0],originalCATID))
                    writeData.append(sim[1])
                    csvResults.writerow(writeData)                
                    #print writeData
        elif operationType == "3":
            for sim in sims:
                if sim[1] != 0.0:
                    if len(dictAnalysis) == 0:
                        print "New entry"
                        """
                        dictAnalysis['key']=sim[0]
                        dictAnalysis['key']['category']=category
                        dictAnalysis['key']['depth']=str(depth)
                        dictAnalysis['key']['idLevel']=str(idLevel)
                        dictAnalysis['key']['ocID']=getOriginalRowFromModel(sim[0],originalCATID)
                        dictAnalysis['key']['nrOcc'] = 1
                        """
                        dictAnalysis[sim[0]] = {'category': category, 'depth': depth, 'idLevel': idLevel, 'ocID': getOriginalRowFromModel(sim[0],originalCATID), 'nrOcc': 1}
                    else:                        
                        print dictAnalysis.keys()
                        """
                        if sim[0] in dictAnalysis.keys():
                            print "Its already in"                        
                            dictAnalysis['key']=sim[0]
                            dictAnalisys['key']['category']=category
                            dictAnalisys['key']['depth']=depth
                            dictAnalisys['key']['idLevel']=idLevel
                            dictAnalisys['key']['originalCatID']=getOriginalRowFromModel(sim[0],originalCATID)
                            dictAnalysis['key']['nrOcc'] += 1
                            dictAnalysis['key']['similarity']+=sim[1]
                        """
        else:
            sys.exit("Unknown flag calculateSimilarity.operationType")

        #garbage collect
        print dictAnalysis
        ifile.close()
        #print "Category: ",category,"    level: ",depth,"     model: ",fileName


#return similarities based on a category comparison; get random documents from category, scattered through levels.
def returnSimilaritiesCategory(category, compareTo="3", limit = "1000"):
    """
    Input:\n 
        category -> BoW representation of document for similarity comparison
        compareTo -> 1: level based comparison (default)
                     2: range based comparison
                     3: both comparisons
        limit ->    Nr. of row to return from database
    """
    #ENVIRONEMNT SETUP
    #variables
    #depthDescirption = []
    #depthID = []    
   
    #get cat debth
    sqlCatDebth = "select max(categoryDepth) from dmoz_categories where Topic like 'Top/"+str(category)+"/%' and filterOut = 0"
    catDepthRow = dbQuery(sqlCatDebth)
    catDepth = catDepthRow[0]
    #print catDepth
    
    #singular comparison, get directory listing where models are stored
    #testData = returnDirectoryList('testData')
    testData = ['0.1']
    #testData = ['0.75', '0.5', '1.0', '0.1', '0.25']

    #get random documents from database for cat; get catid and all files from dmoz_externalpages for each catid
    for depth in range(2,catDepth+1):
        originalContent = []
        originalId = []
        #originalContent, originalId = ""
        #queries
        sqlRandom = "SELECT ep.Description, ep.catid FROM dmoz_externalpages ep LEFT JOIN dmoz_categories c ON ep.catid = c.catid where Topic like 'Top/"+str(category)+"/%' and categoryDepth = "+str(depth)+" and c.filterOut = 0 and ep.filterOut = 0 ORDER BY rand() limit "+limit
        #print sqlRandom
        originalContent, originalId = prepareComparisonDocuments(sqlRandom)
        #print type(originalContent), "    ", originalContent
        #print type(originalId), "    ", originalId
                   
        #start iteration
        for testingDataItem in testData:
            #dynamic file name
            #data to be compared to
            path = "testData/"+str(testingDataItem)+"/"
            fileName = testingDataItem+"_"+category+"_"+str(depth)
            fileNameRange =  testingDataItem+"_"+category+"_1_"+str(depth)

            #load files from disk needed for similarity indexing
            if compareTo == "1":
                calculateSimilarity(path,fileName,originalContent, originalId,category,depth)
            elif compareTo == "2":
                calculateSimilarity(path,fileNameRange,originalContent,originalId,category,depth)
            elif compareTo == "3":
                calculateSimilarity(path,fileName,originalContent, originalId,category,depth)
                calculateSimilarity(path,fileNameRange,originalContent,originalId,category,depth)
            else:
                sys.exit("Something went wrong with similarity calculation. ")

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
        jobs.append(job_server.submit(returnSimilaritiesCategory, (index,), depfuncs = (dbQuery, errorMessage, returnDirectoryList, removePunct, removeStopWords, getMainCat, calculateSimilarity, prepareComparisonDocuments,getOriginalRowFromModel,), modules = ("sys", "os", "glob", "itertools", "csv","gensim.corpora","gensim.models","gensim.similarities","pp", "time", "MySQLdb","nltk","re","nltk.corpus","nltk.stem","string","gc",)))    
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
            4. getOriginalRowFromModel(modelRow="", modelDocument="", file="")
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
        getOriginalRowFromModel(modelRow=6, modelDocument="testData/0.1/origCATID/0.1_News_1_2.csv")
    elif var == "5":
        #myFile= open( "memAnalyzer.txt", "w", 0) 
        #sys.stdout= myFile
        print returnSimilaritiesCategory.__doc__
        returnSimilaritiesCategory("News",compareTo="3", limit = "100")
    elif var == "6":
        print runParallelCategory.__doc__
        runParallelCategory()             
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        
if __name__ == '__main__':    
    main()
    