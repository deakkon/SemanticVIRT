'''
Created on 8.1.2013.

@author: Jurica Seva

PhD Candidate 
Faculty of Organization and Informatics
University of Zagreb

Functions:

1. prepareComparisonDocuments(sql, useVectorModel="")
2. documentVScorpus(document)
'''
#imports
import logging, sys, os, glob
from gensim import corpora, models, similarities
from python.utils.databaseODP import dbQuery
from python.utils.textPrepareFunctions import removeStopWords

#logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#functions     
def prepareComparisonDocuments(sqlQuery):
    """
    Input: 
        sqlQuery to be executed, first parameter being textual data to convert to BoW
        
    Output parameters:
        BoW representation of documents returned from sqlQuery, list of lists
    """
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
    
    #get data from DB
    sqlQueryResults = dbQuery(sqlQuery)
    
    #variabless
    bowTemp = []
    bowReturn = []
        
    #prepare BoW
    for row in sqlQueryResults:
        print "Originalni zapis: ",row[0]
        bowTemp = removeStopWords(row[0])        
        bowReturn.append(bowTemp)            
    
    #print type(bowReturn)
    return bowReturn

#end stuff
def getMainCat():
    #get root categories to be used
    sqlMainCategories = "select distinct(Title) from dmoz_categories where dmoz_categories.categoryDepth = 1 and dmoz_categories.filterOut = 0"
    mainCatRS = dbQuery(sqlMainCategories)
    mainCat = tuple([x[0] for x in mainCatRS])
    return mainCat

#get model files from folder
def getFileList(folder):
    """
    List test model files in folder, with folder being 1000 or 5000
    Input: folder \n 1 -> 1000 \n 2 -> 5000 \n 3 -> all data            
    """
    if folder == "1":
        path = "testData/1000/models/*.tfidf*"
    elif folder == "2":
        path = "testData/5000/models/*.tfidf*"
    elif folder == "3":
         path = "fullDataPP/models/*.tfidf*"
    else:
        sys.exit("Wrong choice. calculateSimilarity.getFileList()")
        
    return [name for name in os.listdir(dir)
                if os.path.isdir(os.path.join(dir, name))]        
    
    print glob.glob(path)
    return glob.glob(path)
        
def returnSimilarities(category, compareTo="1"):
    """
    Input:\n 
        bowDocument -> BoW representation of document for similarity comparison\n
        compareTo -> 1: level based comparison (default) \n
                     2: range based comparison \n
                     3: both comparisons \n
    Output:\n
        Similarity list of documents to selected tfidf model
    """
    #variables
    modelList = []
    depthDescirption = []
    
    #temp dict, corpus, model files for comparison; testing data during programming, 
    #COMMENT DURING ACTUAL COMPARISON
    path = "testData/1000/"
    fileName = "Arts_10"    
    dictPath = path+"dict/"+fileName+".dict"
    corpusPath = path+"corpusFiles/"+fileName+""+".mm"
    modelPath = path+"models/"+fileName+""+".tfidf_model"
    labesPath = path+"labels/"+fileName+""+".csv"
    
    #temp test gensim data
    corpus = corpora.MmCorpus(corpusPath)
    dictionary = corpora.Dictionary.load(dictPath)
    tfidfModel = models.tfidfmodel.TfidfModel.load(modelPath)
    index = similarities.MatrixSimilarity(tfidfModel[corpus])
    
    #get cat debth
    sqlCatDebth = "select max(categoryDepth) from dmoz_categories where Topic like '%/"+str(category)+"/%'"
    catDepthRow = dbQuery(sqlCatDebth)
    catDepth = catDepthRow[0]
    
    #get random documents from database for cat; get catid and all files from dmoz_externalpages for each catid
    for depth in range(2,4):    
        sqlRandom = "SELECT ep.Description, ep.catid FROM dmoz_externalpages ep LEFT JOIN dmoz_categories c ON ep.catid = c.catid where Topic like '%/"+str(category)+"/%' and categoryDepth = "+str(depth)+" ORDER BY rand() LIMIT 1000"
        depthDescirption.append(prepareComparisonDocuments(sqlRandom))
    print type(depthDescirption)
    
    #comparison
    levelIndex = 2
    
    for level in depthDescirption:
        """
        #dynamicm file name
        fileName = category+"_"+levelIndex
        fileNameRange =  category+"_1_"+levelIndex
        
        #load files from disk needed for comaprison and all
        #lOAD MODELS FOR LEVEL levelIndex
        if compareTo == "1" or compareTo == "3":
            corpusPath = path+"corpusFiles/"+fileName+""+".mm"            
            dictPath = path+"dict/"+fileName+".dict"
            modelPath = path+"models/"+fileName+""+".tfidf_model"
            labesPath = path+"labels/"+fileName+""+".csv"
            
            #read in HDD files and create sim index
            corpus = corpora.MmCorpus(corpusPath)
            dictionary = corpora.Dictionary.load(dictPath)            
            tfidfModel = models.tfidfmodel.TfidfModel.load(modelPath)
            index = similarities.MatrixSimilarity(tfidfModel[corpus])            
        
        #lOAD MODELS FOR LEVEL 1_levelIndex
        if compareTo == "2" or compareTo == "3":            
            corpusPathRange = path+"corpusFiles/"+fileNameRange+""+".mm"
            dictPathRange = path+"dict/"+fileNameRange+".dict"
            modelPathRange = path+"models/"+fileNameRange+""+".tfidf_model"
            labesPathRange = path+"labels/"+fileNameRange+""+".csv"

            #read in HDD files and create sim index
            corpusRange = corpora.MmCorpus(corpusPathRange)
            dictionaryRange = corpora.Dictionary.load(dictPath)
            tfidfModelRange = models.tfidfmodel.TfidfModel.load(modelPathRange)
            indexRange = similarities.MatrixSimilarity(tfidfModelRange[corpusRange])              
        """
        
        #compare document for query to selected model
        for dox in level:
            if compareTo == "1" or compareTo == "3":
                #level based comparison
                vec_bow = dictionary.doc2bow(dox)            
                vec_tfidf = tfidfModel[vec_bow]
                sims = index[vec_tfidf]
                sims = sorted(enumerate(sims), key=lambda item: -item[1])            
                print  sims[:20]
                #print "Obradjen zapis: ",dox
                #print "BoW zapis: ",vec_bow
                #print "Mapiran na model: ",vec_tfidf
                #print "Slicnost (Prvih dvadeset: \n",sims[:20]
            
            #range based comparison
            if compareTo == "2" or compareTo == "3":
                vec_bow_range = dictionaryRange.doc2bow(dox)            
                vec_tfidf_range = tfidfModelRange[vec_bow_range]
                sims_range = indexRange[vec_tfidf_range]
                sims_range = sorted(enumerate(sims_range), key=lambda item: -item[1])            
                print  sims_range[:20]
                #print "Obradjen zapis: ",dox
                #print "BoW zapis: ",vec_bow_range
                #print "Mapiran na model: ",vec_tfidf_range
                #print "Slicnost (Prvih dvadeset: \n",sims_range[:20]
                        
        levelIndex += 1

#main 
def main():
    """
    Functions:
        1. prepareComparisonDocuments(sqlQuery)
        2. getFileList(folder)
        3. returnSimilarities()
        Anything else to stop
     """
    print main.__doc__

    var = raw_input("Choose function: ")
        
    if var == "1":
        print prepareComparisonDocuments.__doc__
        var1 = raw_input("Insert SQL query")
        prepareComparisonDocuments(var1)        
    elif var == "2":
        print getFileList.__doc__
        var1 = raw_input("Choose test data version: ")
        getFileList(var1)
    elif var == "3":
        print returnSimilarities.__doc__
        returnSimilarities("Arts")
        
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        

if __name__ == '__main__':    
    main()
    