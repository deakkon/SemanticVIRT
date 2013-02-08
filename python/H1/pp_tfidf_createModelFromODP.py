'''
Created on 9.1.2013.

@author: Jurica Seva

PhD Candidate 
Faculty of Organization and Informatics
University of Zagreb

Functions:
    1. createTFIDFfromODP_dmoz_descriptions(topic="",depthStart="", depthEnd="")
    2. createTrainingData()
'''
#imports
import math, sys, time, csv, os, string, pp, re, gensim, MySQLdb, nltk.corpus, nltk.stem
from MySQLdb import *
#from nltk.corpus import names
#import gensim.corpora
#from gensim import corpora 
#from gensim import models
from nltk.stem import WordNetLemmatizer, PorterStemmer, LancasterStemmer

#stemmers
wnl = nltk.stem.WordNetLemmatizer()
lst = nltk.stem.LancasterStemmer()
ps = nltk.stem.PorterStemmer()


#Database stuff    
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

#vectorization stuff
def createCorpusAndVectorModel(data, fileName ="", outputFormat=1, modelFormat=1):
    """
    Input parameters: sqlQueryResults="", outputFormat=1, modelFormat=1, fileName =""
        1. data -> data to save to models, corpus, dictionary
        2. fileName -> if "" use dummy name
        3. outputFormat definition:     1 -> MmCorpus (default)
                                        2 -> SvmLightCorpus
                                        3 -> BleiCorpus
                                        4 -> LowCorpus
        4. modelFormat:                 1 -> tfidf_model (default)
                                        2 -> lsi
                                        3 -> lda                                                                                                                            
    Output data: saved dictionary, corpus and model files of chosen format to disk, to respected directories
    """   
    #create file names to save
    if fileName == "":
        fileName = "defaultCollection"
    
    #create dictionary
    dictionary = gensim.corpora.Dictionary(data)
    dictFN = "fullDataPP/dict/"+fileName+".dict"
    dictionary.save(dictFN)
    
    #creating dictionary and corpus  files in different matrix formats    
    bow_documents = [dictionary.doc2bow(text) for text in data]
    print "BoW", bow_documents

    #create corpora data for use in creating a vector model representation for furher use
    if outputFormat == 1:
        saveFN = "fullDataPP/corpusFiles/"+fileName+".mm"
        gensim.corpora.MmCorpus.serialize(saveFN, bow_documents)
    elif outputFormat == 2:
        saveFN = "fullDataPP/corpusFiles/"+fileName+".svmlight"
        gensim.corpora.SvmLightCorpus.serialize(saveFN, bow_documents)
    elif outputFormat == 3:
        saveFN = "fullDataPP/corpusFiles/"+fileName+".lda-c"
        gensim.corpora.BleiCorpus.serialize(saveFN, bow_documents)
    elif outputFormat == 4:
        gensim.corpora.LowCorpus.serialize(saveFN, bow_documents)
        saveFN = fileName+".low" 
    else:
        errorMessage("Something went wrong with the type identificator")
    
    #save model to disk -> model of all documents that are going to be compared against
    if modelFormat == 1:
        tfidf = gensim.models.TfidfModel(bow_documents)
        saveFN = "fullDataPP/models/"+fileName+".tfidf_model"
        tfidf.save(saveFN)
    elif modelFormat == 2:
        #lsi
        lsi = gensim.models.LsiModel(bow_documents)
        saveFN = "fullDataPP/models/"+fileName+".lsi"
        lsi.save(saveFN)
    elif modelFormat == 3:
        #lsi
        lda = gensim.models.LdaModel(bow_documents)
        saveFN = "fullDataPP/models/"+fileName+".lda"
        lda.save(saveFN)
    else:
        errorMessage("createTrainingModel: Something went wrong with the type identificator")
    
        
def getCategoryLabel(categoryLabels,fileName):
    """
    categoryLabels -> list of labels to write to disk
    fileName -> file to save labels returned by the query
    """
    #path to save the file    
    if os.path.realpath(__file__)== "/home/jseva/SemanticVIRT/python/utils/createVectorModel.py":
        fileName = "../H1/fullDataPP/labels/"+fileName+".csv"
    else:
        fileName = "fullDataPP/labels/"+fileName+".csv"    
    
    #filenames
    out = csv.writer(open(fileName,"w"), delimiter=',',quoting=csv.QUOTE_ALL)
    
    writeLabels = []
    
    for row in categoryLabels:
        for i in row:            
            if i != "" or i.lower() not in string.letters.lower():
                writeLabels.append(i.lower())

    out.writerow(writeLabels)


#end stuff
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
    
    #get max debth
    sqlmaxDepth = "select max(categoryDepth) from dmoz_categories where Topic like '%/"+str(category)+"/%' and filterOut = 0"
    maxDebthRS = dbQuery(sqlmaxDepth)
    maxDebth = maxDebthRS[0]
    
    #(1,indeks) list variables
    dataCategoryLevelAll = []
    dataCategoryLabelAll = []
    #counter
    indeks = 2

    #go through all levels (2,maxDebth)
    while indeks <= maxDebth:                
        #create file names
        fileNameAll = category+"_1_"+str(indeks)
        fileNameLevel = category+"_"+str(indeks) 
        
        #level list variables
        dataCategoryLevel = []
        dataCategoryLabel = []
        
        #dynamic SQL queries
        sqlCategoryLevel = "select Description,Title,link from dmoz_externalpages where catid in (select catid from dmoz_categories where Topic like '%/"+category+"/%' and categoryDepth = "+str(indeks)+" and filterOut = 0)"            
        sqlCategoryLabel = "select distinct(Title) from dmoz_categories where Topic like '%/"+category+"/%' and categoryDepth = "+str(indeks)+ " and filterOut = 0"
        #print sqlCategoryLevel
        #print sqlCategoryLabel
        

        #getData
        sqlQueryResultsLevel = dbQuery(sqlCategoryLevel)
        sqlQueryResultsLabel = dbQuery(sqlCategoryLabel)

        #####################################################
        #prepare returned documents
        #data for individual level
        for row in sqlQueryResultsLevel:
            dataCategoryLevel.append(removeStopWords(row[0]))
        
        #create models for individual level
        createCorpusAndVectorModel(dataCategoryLevel, fileName=fileNameLevel)
        
        #data for individual level labels
        for row in sqlQueryResultsLabel:
            if type(row) is not long:
                dataCategoryLabel.append(removeStopWords(row[0]))
               
        #create labels for individual level
        getCategoryLabel(dataCategoryLabel,fileNameLevel)
        #####################################################
        #####################################################
        #data for all levels, labels so far
        dataCategoryLevelAll.extend(dataCategoryLevel)
        dataCategoryLabelAll.extend(dataCategoryLabel)
        
        #create models, corpus, dicts, labels for all levels
        createCorpusAndVectorModel(dataCategoryLevelAll, fileName=fileNameAll)
        getCategoryLabel(dataCategoryLabelAll,fileNameAll)
        #####################################################
        
        #increment counter indeks by 1        
        indeks += 1

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
    print index
    jobs.append(job_server.submit(createData, (index,), depfuncs = (dbQuery,createCorpusAndVectorModel,getCategoryLabel,removeStopWords,removePunct,dbQuery,errorMessage,), modules = ("math", "sys", "time", "csv", "os", "string", "pp","gensim","MySQLdb","gensim.corpora","gensim.models","re","nltk.corpus","nltk.stem",)))

for job in jobs:
    result = job()
    if result:
        break
#prints
job_server.print_stats()
print "Time elapsed: ", time.time() - start_time, "s"