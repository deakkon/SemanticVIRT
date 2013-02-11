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
import logging, sys, os, glob, itertools, csv
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
    
    #variables
    originalContent = []
    originalID = []
    depthDescirption = []
    depthID = []    
    modelList = []
        
    #prepare BoW
    for row in sqlQueryResults:
        if type(row) is not long:
            #print "Originalni zapis: ",row[0]
            bowTemp = removeStopWords(row[0])        
            bowReturn.append(bowTemp)
            #original catid
            originalID.append(row[1])
    #print type(bowReturn)
    return (bowReturn,originalID)

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
    originalContent = []
    originalID = []
    depthDescirption = []
    depthID = []    
    modelList = []
        
    #get cat debth
    sqlCatDebth = "select max(categoryDepth) from dmoz_categories where Topic like '%/"+str(category)+"/%' and filterOut = 0"
    catDepthRow = dbQuery(sqlCatDebth)
    catDepth = catDepthRow[0]
    
    #get random documents from database for cat; get catid and all files from dmoz_externalpages for each catid
    for depth in range(2,catDepth):    
        sqlRandom = "SELECT ep.Description, ep.catid FROM dmoz_externalpages ep LEFT JOIN dmoz_categories c ON ep.catid = c.catid where Topic like '%/"+str(category)+"/%' and categoryDepth = "+str(depth)+" and and c.filterOut = 0 and ep.filterOut = 0 ORDER BY rand() LIMIT 1000"
        originalContent, originalId = prepareComparisonDocuments(sqlRandom)
        depthDescirption.append(originalContent)
        depthID.append(originalId)
        
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
            corpus = corpora.MmCorpus(corpusPath)
            dictionary = corpora.Dictionary.load(dictPath)            
            tfidfModel = models.tfidfmodel.TfidfModel.load(modelPath)
            index = similarities.MatrixSimilarity(tfidfModel[corpus])
            
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
            corpusRange = corpora.MmCorpus(corpusPathRange)
            dictionaryRange = corpora.Dictionary.load(dictPathRange)
            tfidfModelRange = models.tfidfmodel.TfidfModel.load(modelPathRange)
            indexRange = similarities.MatrixSimilarity(tfidfModelRange[corpusRange])

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
                for sim in sims:
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
                #sims_range.save(path+"sim/"+fileNameRange)
                #print  sims_range[:20]
                for sim in sims:
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
        indeks = getMainCat()
        for i in indeks:
            returnSimilarities(i,"3")
        
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        

if __name__ == '__main__':    
    main()
    