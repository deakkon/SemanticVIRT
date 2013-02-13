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
import logging, sys, os, glob, itertools, csv, pp, time, gensim.corpora, gensim.models, gensim.similarities, MySQLdb, nltk

#logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#database functionality
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
        sys.exit(1)

def errorMessage(msg):
    print msg
    sys.exit(1)

#prepare stuff

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
    
    #str to list
    if type(text) is str:
        text = text.split()        
        text = [x.lower() for x in text]        

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
    #print "remove punct",content
    content = [w for w in content if w.lower() not in stopwords]
    #print "remove sw",content
    content = [ps.stem(i) for i in content]
    #print "SW ",content
    return content

def getMainCat():
    """
    Returns main categories from ODP; input for PP pipeline
    """
    sqlMainCategories = "select distinct(Title) from dmoz_categories where dmoz_categories.categoryDepth = 1 and dmoz_categories.filterOut = 0"
    mainCatRS = dbQuery(sqlMainCategories)
    mainCat = tuple([x[0] for x in mainCatRS])
    return mainCat

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

#get model files from folder

def returnSimilarities(category, compareTo="1", percentage = ""):
    """
    Input:\n 
        bowDocument -> BoW representation of document for similarity comparison\n
        compareTo -> 1: level based comparison (default) \n
                     2: range based comparison \n
                     3: both comparisons \n
        percentage -> % of pages to randomly get from database for specific level for specific category
    Output:\n
        Similarity list of documents to selected tfidf model
    """
    #variables
    originalContent = []
    originalId = []
    depthDescirption = []
    depthID = []    
    #modelList = []       

    #get cat debth
    sqlCatDebth = "select max(categoryDepth) from dmoz_categories where Topic like '%/"+str(category)+"/%' and filterOut = 0"
    catDepthRow = dbQuery(sqlCatDebth)
    catDepth = catDepthRow[0]
    
    #get random documents from database for cat; get catid and all files from dmoz_externalpages for each catid
    for depth in range(2,catDepth):
        """
        #number of elements to return from database; if percentage != '' then % else 1000
        if percentage == "":
            limit = 1000
        elif percentage != "":
            sqlPercent = "select count(*) from dmoz_categories where Topic like '%/"+str(category)+"/%' and categoryDepth = "+str(depth)
            #numerRows = dbQuery(sqlPercent)            
        elif percentage > 100:
            sys.exit("Percentage can not be more than 100%")
        """

        #queries
        sqlRandom = "SELECT ep.Description, ep.catid FROM dmoz_externalpages ep LEFT JOIN dmoz_categories c ON ep.catid = c.catid where Topic like '%/"+str(category)+"/%' and categoryDepth = "+str(depth)+" and c.filterOut = 0 and ep.filterOut = 0 ORDER BY rand() LIMIT 1000"
        print sqlRandom
        originalContent, originalId = prepareComparisonDocuments(sqlRandom)
        depthDescirption.append(originalContent)
        depthID.append(originalId)
        
    #temp dict, corpus, model files for comparison; testing data during programming, 
    #COMMENT DURING ACTUAL COMPARISON
    path = "testData/1000/"
    """
    fileName = "Arts_10"    
    dictPath = path+"dict/"+fileName+".dict"
    corpusPath = path+"corpusFiles/"+fileName+""+".mm"
    modelPath = path+"models/"+fileName+""+".tfidf_model"
    labesPath = path+"labels/"+fileName+""+".csv"

    #temp test gensim data
    corpus = gensim.corpora.MmCorpus(corpusPath)
    dictionary = gensim.corpora.Dictionary.load(dictPath)
    tfidfModel = gensim.models.tfidfmodel.TfidfModel.load(modelPath)
    index = gensim.similarities.MatrixSimilarity(tfidfModel[corpus])
    """    
    levelIndex = 2
    
    for levelC, levelID in itertools.izip(depthDescirption,depthID):
                
        #dynamic file name
        fileName = category+"_"+str(levelIndex)
        fileNameRange =  category+"_1_"+str(levelIndex)
        
        #load files from disk needed for similarity indexing
        #lOAD MODELS FOR LEVEL levelIndex
        if compareTo == "1" or compareTo == "3":
            corpusPath = path+"corpusFiles/"+fileName+""+".mm"            
            dictPath = path+"dict/"+fileName+".dict"
            modelPath = path+"models/"+fileName+""+".tfidf_model"
            labesPath = path+"labels/"+fileName+""+".csv"
            resultsSavePath = path+"sim/"+fileName+".csv"
            
            #read in HDD files and create sim index
            corpus = gensim.corpora.MmCorpus(corpusPath)
            dictionary = gensim.corpora.Dictionary.load(dictPath)            
            tfidfModel = gensim.models.tfidfmodel.TfidfModel.load(modelPath)
            index = gensim.similarities.MatrixSimilarity(tfidfModel[corpus],num_features=len(dictionary))
            
            #number of similarity records for further processing
            if percentage != "":
                sample = (percentage * len(dictionary))/100
            elif percentage == "":
                percentage = 0.05
                sample = (percentage * len(dictionary))/100           
            
            #create csv
            csvResults = csv.writer(open(resultsSavePath,"w"), delimiter=',',quoting=csv.QUOTE_ALL)
            csvResults.writerow(('category','level','catidEP','matrixID','similarity'))
            
        #lOAD MODELS FOR LEVEL 1_levelIndex
        if compareTo == "2" or compareTo == "3":            
            corpusPathRange = path+"corpusFiles/"+fileNameRange+""+".mm"
            dictPathRange = path+"dict/"+fileNameRange+".dict"
            modelPathRange = path+"models/"+fileNameRange+""+".tfidf_model"
            labesPathRange = path+"labels/"+fileNameRange+""+".csv"
            resultsRangeSavePath = path+"sim/"+fileNameRange+".csv"

            #read in HDD files and create sim index
            corpusRange = gensim.corpora.MmCorpus(corpusPathRange)
            dictionaryRange = gensim.corpora.Dictionary.load(dictPathRange)
            tfidfModelRange = gensim.models.tfidfmodel.TfidfModel.load(modelPathRange)
            indexRange = gensim.similarities.MatrixSimilarity(tfidfModelRange[corpusRange],num_features=len(dictionaryRange))
            
            #number of similarity records for further processing
            if percentage != "":
                sampleRange = (percentage * len(dictionaryRange))/100
            elif percentage == "":
                percentage = 0.05
                sampleRange = (percentage * len(dictionaryRange))/100              

            #create csv
            csvResultsRange = csv.writer(open(resultsRangeSavePath,"w"), delimiter=',',quoting=csv.QUOTE_ALL)
            csvResultsRange.writerow(('category','level','catidEP','matrixID','similarity'))
        #print "##############################"
        
        #CONTENT PART; CALCULATE SIMILARTIY BASED ON TFIDF
        #RETURN TOP(n) DOCUMENTS BY SIMILARITY
        for descriptionLevel, idLevel in  itertools.izip(levelC,levelID):
            #print idLevel,"    ",descriptionLevel 
            if compareTo == "1" or compareTo == "3":
                #print 'compareTo == "1" or compareTo == "3"'
                #level based comparison
                vec_bow = dictionary.doc2bow(descriptionLevel)            
                vec_tfidf = tfidfModel[vec_bow]
                sims = index[vec_tfidf]
                sims = sorted(enumerate(sims), key=lambda item: -item[1])            
                #print  sims[:20]
                #print "Obradjen zapis: ",dox
                #print "BoW zapis: ",vec_bow
                #print "Mapiran na model: ",vec_tfidf
                #print "Slicnost (Prvih dvadeset: \n",sims[:20]
                #WRITE SIMLARITY RESULTS TO CSV
                for sim in sims[:sample]:
                    writeData = []
                    #print sim[0], sim[1]
                    writeData.append(category)
                    writeData.append(levelIndex)
                    writeData.append(idLevel)
                    writeData.append(sim[0])
                    writeData.append(sim[1])
                    csvResults.writerow(writeData)
            
            #range based comparison
            if compareTo == "2" or compareTo == "3":
                #print 'compareTo == "2" or compareTo == "3"'
                vec_bow_range = dictionaryRange.doc2bow(descriptionLevel)            
                vec_tfidf_range = tfidfModelRange[vec_bow_range]
                sims_range = indexRange[vec_tfidf_range]
                sims_range = sorted(enumerate(sims_range), key=lambda item: -item[1])
                sims_range.save(path+"sim/"+fileNameRange)
                #print  sims_range[:20]
                for sim in sims_range[:sampleRange]:
                    writeData = []
                    #print sim[0], sim[1]
                    writeData.append(category)
                    writeData.append(levelIndex)
                    writeData.append(idLevel)
                    writeData.append(sim[0])
                    writeData.append(sim[1])
                    csvResults.writerow(writeData)                    
                #print "Obradjen zapis: ",dox
                #print "BoW zapis: ",vec_bow_range
                #print "Mapiran na model: ",vec_tfidf_range
                #print "Slicnost (Prvih dvadeset: \n",sims_range[:20]
                #WRITE SIMLARITY RESULTS TO CSV

        levelIndex += 1

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
    #inputs =("Arts",)
    
    jobs = []
    
    for index in inputs:
        #print index
        jobs.append(job_server.submit(returnSimilarities, (index,), depfuncs = (dbQuery, errorMessage, removePunct, removeStopWords, getMainCat, prepareComparisonDocuments,), modules = ("logging", "sys", "os", "glob", "itertools", "csv","gensim.corpora","gensim.models","gensim.similarities","pp", "time", "MySQLdb","nltk","re","nltk.corpus","nltk.stem","string",)))    
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
            4. returnSimilarities(category, compareTo="1")
            5. runParallel()
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
        print returnSimilarities.__doc__
        returnSimilarities("Arts")
    elif var == "5":
        print runParallel.__doc__
        runParallel()             
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        
if __name__ == '__main__':    
    main()