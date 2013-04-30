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
    
def prepareSubcategory(category):
    allTheLetters = string.uppercase
    #print allTheLetters
    
    try:
        gc.collect()
        con = MySQLdb.connect(host="localhost", user="root", passwd="root", db="dmoz")
        con.autocommit(True)
        cur = con.cursor()  
    
    except MySQLdb.Error, e:
        print "Error dbConnect %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    sql = "select distinct(Topic) from dmoz_categories where mainCategory = '%s' and categoryDepth = '2'" %(category)
    #print sql
    sqlRez = dbQuery(sql)
    
    #cur.execute("ALTER TABLE dmoz_combined_level2 DISABLE KEYS;")
    #cur.execute("SET UNIQUE_CHECKS = 0;")
    #cur.execute("SET AUTOCOMMIT = 0;")
    
    for rez in sqlRez:
        #print rez
        data = rez[0].split("/")
        print rez[0],"\t",data[2]
        if data[2] in allTheLetters:
            updateCatIDRows = 'select catid from dmoz_categories where Topic = "'+str(rez[0])+'"'
        else:
            updateCatIDRows = 'select catid from dmoz_categories where Topic like "'+str(rez[0])+'%"'
            
        print updateCatIDRows
        rezUpdateCatIDRows = dbQuery(updateCatIDRows)
        if rezUpdateCatIDRows != 0:
            params = [(data[2], row[0]) for row in rezUpdateCatIDRows]
            #print params
            sqlUpdate = 'update dmoz_combined_level2 set subCategory = %s where catid =%s'
            #print sqlUpdate
            cur.executemany(sqlUpdate,params)
            #cur.commit()

    #cur.execute("ALTER TABLE dmoz_combined_level2 ENABLE KEYS;")
    #cur.execute("SET UNIQUE_CHECKS = 1;")
    #cur.execute("SET FOREIGN_KEY_CHECKS = 1;")
    #cur.execute("SET AUTOCOMMIT = 1;")
    #cur.execute("COMMIT;")

#prepare text for gensimn stuff
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

def createCorpusAndVectorModel(data, path, fileName, outputFormat=1, modelFormat=1):
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
    #path = "testData2/%s/%s/" %(groupingType,dataSet)
    
    #create file names to save
    if fileName == "":
        sys.exit("No file name given.")
    
    #create dictionary
    dictionary = gensim.corpora.Dictionary(data)
    dictFN = "%sdict/%s.dict" %(path,fileName)
    dictionary.save(dictFN)
    
    #creating dictionary and corpus  files in different matrix formats    
    bow_documents = [dictionary.doc2bow(text) for text in data]

    #create corpora data for use in creating a vector model representation for furher use
    corpora = "%scorpusFiles/%s"%(path,fileName)
    if outputFormat == 1:
        saveCorpora = "%s.mm" %(corpora)
        gensim.corpora.MmCorpus.serialize(saveCorpora, bow_documents)
    elif outputFormat == 2:
        saveCorpora = "%s.svmlight" %(corpora)
        gensim.corpora.SvmLightCorpus.serialize(saveCorpora, bow_documents)
    elif outputFormat == 3:
        saveCorpora = "%s.lda-c" %(corpora)
        gensim.corpora.BleiCorpus.serialize(saveCorpora, bow_documents)
    elif outputFormat == 4:
        saveCorpora = "%s.low" %(corpora)
        gensim.corpora.LowCorpus.serialize(saveCorpora, bow_documents)
    else:
        errorMessage("Something went wrong with the corpus type identificator")
    
    #save model to disk -> model of all documents that are going to be compared against
    model = "%smodels/%s"%(path,fileName)
    if modelFormat == 1:
        tfidf = gensim.models.TfidfModel(bow_documents)
        saveModel = model+".tfidf_model"
        tfidf.save(saveModel)
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

def getCategoryLabel(categoryLabels,fileName, dataSet):
    """
    categoryLabels -> list of labels to write to disk
    fileName -> file to save labels returned by the query
    """
    #lables array for level, for % of accesed rows
    writeLabels = []    

    #file to save data to 
    fileName = "testData2/"+str(dataSet)+"/labels/"+fileName+".csv"
    out = csv.writer(open(fileName,"w"), delimiter=',',quoting=csv.QUOTE_ALL)

    for row in categoryLabels:
        for i in row:            
            if i != "" or i.lower() not in string.letters.lower():
                writeLabels.append(i.lower())

    out.writerow(writeLabels)

def getCategoryListLevel(catID,path,fileName):
    """
    catID: original cadID while creating data
    fileName: fileName for saving
    dataset: % model of data
    """
    #create csv
    resultsSavePath = "%s/origCATID/%s.csv" %(path,fileName)
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
    
def createDir(dir):
    #basic directory for grouping type: GENERAL
    path = "%s" %(dir)
    if not os.path.isdir(path):
        os.mkdir(path)

def getMainCat():
    #get root categories to be used
    sqlMainCategories = "select distinct(mainCategory) from dmoz_combined_level2 where categoryDepth = 2"
    mainCatRS = dbQuery(sqlMainCategories)
    mainCat = tuple([x[0] for x in mainCatRS])
    return mainCat

def getSubCat(category):
    #get sub_categories to be used
    sqlMainCategories = "select distinct(subCategory) from dmoz_combined_level2 where mainCategory = '%s' and subCategory is not null" %(category)
    mainCatRS = dbQuery(sqlMainCategories)
    mainCat = tuple([x[0] for x in mainCatRS])
    return mainCat

def getMaxDebth(category,subcategory):
    #get root categories to be used
    sqlMainCategories = "select max(categoryDepth) from dmoz_combined_level2 where mainCategory = '%s' and subCategory = '%s'" %(category,subcategory)
    mainCatRS = dbQuery(sqlMainCategories)
    mainCat = tuple([x[0] for x in mainCatRS])
    return mainCat

def createData(category,subcategory):
    """
    1. get root categories to be used and iterate through main categories
    3. get max depth for individual category
    4. from 1 to max till 1 to 1
        get all catid for iterated category
        get all pages for selected categories
        call createCorpusAndVectorModel from selected documents
    """
    path = "testData2/"
    
    #FULL DATA
    percentageList = [0.1, 0.25, 0.5, 0.75, 1.0]
    GROUPTYPE = ["CATID","FATHERID","GENERAL"]
    
    #DUMMY TEST DATA
    #percentageList = [0.1]
    #GROUPTYPE = ["CATID"]

    #go through all levels (2,maxDebth)
    for group in GROUPTYPE:
        
        groupPath = "%s%s/" %(path,group)
        createDir(groupPath)
            
        scMaxDebth = getMaxDebth(category,subcategory)
        #print scMaxDebth
        ranger = [x for x in range(3,scMaxDebth[0]+1)]
        
        if group != "FATHERID":
            sqlCategoryLevel = "select Description, catid, categoryDepth from dmoz_combined_level2 where mainCategory = '%s' and subCategory = '%s'" %(category,subcategory)
        else:
            sqlCategoryLevel = "select Description, fatherid, categoryDepth from dmoz_combined_level2 where mainCategory = '%s' and subCategory = '%s'" %(category,subcategory)
        #print sqlCategoryLevel
        sqlQueryResultsLevel = dbQuery(sqlCategoryLevel)
        #print "lenght %i " %(len(sqlQueryResultsLevel))
        if sqlQueryResultsLevel == 0:
            print category,"\t",indeks,"\t",sqlCategoryLevel
            sys.exit("SQL code error")
            
        #specific % models
        for percentageItem in percentageList:
            #print percentageItem
            pPath = "%s%s/" %(groupPath, percentageItem)
            createDir(pPath)
            #print pPath
            categoryPath = "%s%s/" %(pPath,category)
            createDir(categoryPath)
            #print categoryPath
            
            #path to dict, model, corpusFiles directory, sim, labels, origCATID directories
            pathSubDir = ["dict/","models/","corpusFiles/","origCATID/","sim/"]
            for pathItem in pathSubDir:
                checkPath = "%s%s" %(categoryPath,pathItem)
                createDir(checkPath)
            
            dataCategoryLevelAll = []
            dataCategoryLabelAll = []
            originalCatIDAll = []
            dataCategorySingleAll = []

            for indeks in ranger:
                
                #list of data for specific level
                dataLevel = [x for x in sqlQueryResultsLevel if x[2] == indeks]
                print category,"\t",subcategory,"\t",indeks,"\t",len(dataLevel),"\t",percentageItem,"\t",group
                
                if len(dataLevel) != 0:
                    
                    #level list variables
                    dataCategoryLevel = []
                    dataCategoryLabel = []
                    originalCatID = []
                    originalFatherID = []
                    tempContent = []
                    
                    #get unique values
                    if group == "GENERAL":
                        #calculate percentage per catid
                        percentageLevel = int(percentageItem * int((len(dataLevel))))
                        
                        if percentageLevel == 0:
                            percentageLevel = 1

                        tempContent = [row[0] for row in dataLevel[:percentageLevel]]
                        originalCatID = [row[1] for row in dataLevel[:percentageLevel]]
                        dataCategoryLevel.append(removeStopWords(tempContent))
                        print uniq,"\t",len(tempContent),"\t" 
                    else:
                        unique = [] 
                        for row in dataLevel:
                            if row[1] not in unique:
                                unique.append(row[1])
                        
                        #prepare rows with uniq for document in model
                        for uniq in unique:
                            tempContent = []
                            
                            tempContent = [row[0] for row in dataLevel if row[1] == uniq]
                            print uniq,"\t",len(tempContent),"\t"
                            
                            #calculate percentage per catid
                            percentageLevel = int(percentageItem * int((len(tempContent))))
                            if percentageLevel == 0:
                                percentageLevel = 1

                            tempContent = " ".join(tempContent[:percentageLevel])
                            dataCategoryLevel.append(removeStopWords(tempContent))
                            originalCatID.append(uniq)

                    #create file names
                    fileNameAll = str(percentageItem)+"_"+subcategory+"_1_"+str(indeks)
                    fileNameLevel = str(percentageItem)+"_"+subcategory+"_"+str(indeks)
                    
                    #create corpus models
                    createCorpusAndVectorModel(dataCategoryLevel,categoryPath,fileNameLevel)
                    dataCategoryLevelAll.extend(dataCategoryLevel)
                    createCorpusAndVectorModel(dataCategoryLevelAll,categoryPath, fileNameAll)
        
                    ##########   ORIGINAL CATEGORIES ID   #################
                    getCategoryListLevel(originalCatID,categoryPath,fileNameLevel)
                    originalCatIDAll.extend(originalCatID)
                    getCategoryListLevel(originalCatIDAll,categoryPath,fileNameAll)
        
                    #print out number of documents for (cat,level,model)
                    #print category,"    ",indeks,"    ",percentageItem,"    ",len(sqlQueryResultsLevel),"    ",len(dataCategoryLevel),"    ",len(originalCatID),"    ",len(dataCategoryLevelAll),"    ",len(originalCatIDAll)
                    
                    del tempContent
                    del originalCatID
                    del dataCategoryLevel
                    del originalFatherID
                    gc.collect()
                
                else:
                    print "No rows for %s\t%s\t%i." %(category,subcategory,indeks)
                
            del dataCategoryLevelAll
            del dataCategoryLabelAll
            del originalCatIDAll
            del dataCategorySingleAll
            gc.collect()                


#PARALEL PYTHON
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
        subCat = getSubCat(index)
        for sc in subCat:
            jobs.append(job_server.submit(createData, (index,sc), depfuncs = (dbQuery,createCorpusAndVectorModel,getCategoryLabel,removeStopWords,removePunct,dbQuery,errorMessage,getCategoryListLevel,createDir,getSubCat, getMainCat,getMaxDebth,), modules = ("math", "sys", "time", "csv", "os", "string", "pp","gensim","MySQLdb","gensim.corpora","gensim.models","re","nltk.corpus","nltk.stem","itertools","urlparse","gc",)))
    
    for job in jobs:
        result = job()
        if result:
            break
    #prints
    job_server.print_stats()
    print "Time elapsed: ", time.time() - start_time, "s"


def runPP_SubCat():
    """
    Run comparison on n processors
    Update dmoz_combined_level2 with subcategory descriptors
    """
    # tuple of all parallel python servers to connect with
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
    
    inputs = getMainCat()
    print inputs
    #inputs = "Arts"
    jobs = []

    for index in inputs:
        jobs.append(job_server.submit(prepareSubcategory, (index,), depfuncs = (dbQuery,), modules = ("math", "sys", "time", "csv", "os", "string", "pp","gensim","MySQLdb","gensim.corpora","gensim.models","re","nltk.corpus","nltk.stem","itertools","urlparse","gc",)))

    #print jobs
    #job_server.wait()
    i = 0
    for job in jobs:
        print "Process %i" %(i)
        print job
        job()
        i += 1

    #prints
    job_server.print_stats()
    print "Time elapsed: ", time.time() - start_time, "s"



#main UI

def main():
    """
    Functions:
        1. createData(category)
        2. runParallel()
        7. getMainCat()
        8. prepareSubcategory()
            Anything else to stop
     """
    print main.__doc__

    var = raw_input("Choose function: ")
        
    if var == "1":
        print createData.__doc__
        createData("Arts","Illustration")
    elif var == "2":
        print runParallel.__doc__
        runParallel()    
    elif var == "7":
        getMainCat.__doc__
        print getMainCat()
    elif var == "8":
        #myFile= open("new.txt", "w") 
        #sys.stdout= myFile
        runPP_SubCat()
    elif var == "9":
        cat = raw_input("Insert category: ")
        prepareSubcategory(cat)
    else:
        print "Hm, ", var," not supported as an option"
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':    
    main()