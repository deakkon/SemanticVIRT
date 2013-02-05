'''
Created on 2.1.2013.

@author: Jurica

Functions:
    1.vectorizeDocument(document)
    2.createCorpusAndVectorModel(documents, outputFormat=1, modelFormat=1, fileName ="")

'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#imports
import logging, sys, csv, numpy, scipy, matplotlib, datetime
from scipy import stats
from scipy.stats.stats import gmean, hmean, skew, kurtosis, kurtosistest
matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.mlab
from numpy.random import normal
#user functions
from gensim import corpora, models
from python.utils.textPrepareFunctions import removePunct, removeStopWords 
from python.utils.databaseODP import dbQuery, errorMessage

#logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#functions
def getCatInfo():
    """
    Get basic statistics for each category
    No user input expected
    Sources:     1. SQL query
                    -> main topics
                    -> depth per topic
                    -> number of documents per main topic
                    -> number of labels/subcategories per main topic
                    -> number of labels/subcategories per main topic per depth level
                2. Corpus files
                    -> to be dtermined
    """
    #variables
    categories = []
    
    #get root categories to be used
    sqlMainCategories = "select distinct(Title) from dmoz_categories where dmoz_categories.categoryDepth = 1 and dmoz_categories.filterOut = 0"
    mainCat = dbQuery(sqlMainCategories)
        
    #iterate through main categories
    categories = [row[0] for row in mainCat]
    """
    for cat in mainCat:
        print cat[0]
        sqlmaxDepth = "select max(categoryDepth) from dmoz_categories where Topic like '%/"+str(cat[0])+"/%' and filterOut = 0"
        maxDebthRS = dbQuery(sqlmaxDepth)
        maxDebth = maxDebthRS[0]
        print "Category: ", cat[0],"Depth level: ",maxDebth
        categories.append(cat[0])
    """    
    return categories
        
def getDescriptiveStatisticsCategory():
    """
    Basic statistics for each category, level based:
        1. Mean
        2. Min
        3. Max
        4. Variance
        5. Std. variation
        6. Median
    """
    #variables
    categories = getCatInfo()
    finalResults = []
    
    for cat in categories:
        #variables, specific for cat
        perCategory = []
        tempResults = []
        sqlMaxDepth = "select max(categoryDepth) from dmoz_categories where Topic like '%/"+str(cat)+"/%' and filterOut = 0"
        #query results
        maxDebthRS = dbQuery(sqlMaxDepth)
        #for each depth level
        for depth in range(1,maxDebthRS[0]):
            sqlDepth = "select count(*) from dmoz_categories where Topic like '%/"+str(cat)+"/%' and filterOut = 0 and categoryDepth="+str(depth)
            debthRowCount = dbQuery(sqlDepth)
            perCategory.append(debthRowCount[0])
        perCategoryNumpy = numpy.asarray([perCategory[x] for x in range(1,len(perCategory))])
        #test print
        print "##################################################"
        print perCategoryNumpy                
        print("Mean : {0:8.6f}".format(perCategoryNumpy.mean()))
        tempResults.append("{0:8.6f}".format(perCategoryNumpy.mean()))
        print("G Mean : {0:8.6f}".format(gmean(perCategoryNumpy)))
        tempResults.append(format(gmean(perCategoryNumpy)))
        print("H Mean : {0:8.6f}".format(hmean(perCategoryNumpy)))
        tempResults.append(format(hmean(perCategoryNumpy)))
        print("Median : {0:8.6f}".format(scipy.median(perCategoryNumpy)))
        tempResults.append(format(scipy.median(perCategoryNumpy)))                
        print("Minimum : {0:8.6f}".format(perCategoryNumpy.min()))
        tempResults.append(format(perCategoryNumpy.min()))
        print("Maximum : {0:8.6f}".format(perCategoryNumpy.max()))
        tempResults.append(format(perCategoryNumpy.max()))
        print("Std. deviation : {0:8.6f}".format(perCategoryNumpy.std()))
        tempResults.append(format(perCategoryNumpy.std()))
        print("Skewness : {0:8.6f}".format(skew(perCategoryNumpy)))
        tempResults.append(format(skew(perCategoryNumpy)))
        print("Kurtosis : {0:8.6f}".format(kurtosis(perCategoryNumpy)))
        tempResults.append(format(kurtosis(perCategoryNumpy))) 
        tempResults.append(cat)
        print "########################################"
        finalResults.append(tempResults)
        
    #create file name
    fileName = "statistics/CAT_DescriptiveStatistics"+datetime.datetime.now().ctime()+".csv"
    #print fileName
    #write to csv
    out = csv.writer(open(fileName,"wb"), delimiter=';',quoting=csv.QUOTE_NONE)

    out.writerow(['Mean','Geometric mean','Harmonic mean','Median','Minimum','Maximum','Std. deviation','Skewness','Kurtosis','Category'])
    for results in finalResults:      
        out.writerow(results)
        
def getDescriptiveStatisticsEP():
    """
    Basic statistics for dmoz_externalpages, level based:
        1. Mean
        2. Min
        3. Max
        4. Variance
        5. Std. variation
        6. Median
    """                 
    #variables
    categories = getCatInfo()
    finalResults = []
    
    for cat in categories:
        #variables, specific for cat
        perCategory = []
        tempResults = []
        sqlMaxDepth = "select max(categoryDepth) from dmoz_categories where Topic like '%/"+str(cat)+"/%' and filterOut = 0"
        #query results
        maxDebthRS = dbQuery(sqlMaxDepth)
        #for each depth level
        for depth in range(1,maxDebthRS[0]):
            sqlDepth = "select count(*) from dmoz_externalpages where catid in (select catid from dmoz_categories where Topic like '%/"+str(cat)+"/%' and categoryDepth="+str(depth)+")"
            debthRowCount = dbQuery(sqlDepth)
            perCategory.append(debthRowCount[0])        
        perCategoryNumpy = numpy.asarray([perCategory[x] for x in range(1,len(perCategory))])        
        #test print
        print "##################################################"
        print perCategoryNumpy                
        print("Mean : {0:8.6f}".format(perCategoryNumpy.mean()))
        tempResults.append("{0:8.6f}".format(perCategoryNumpy.mean()))
        print("G Mean : {0:8.6f}".format(gmean(perCategoryNumpy)))
        tempResults.append(format(gmean(perCategoryNumpy)))
        print("H Mean : {0:8.6f}".format(hmean(perCategoryNumpy)))
        tempResults.append(format(hmean(perCategoryNumpy)))
        print("Median : {0:8.6f}".format(scipy.median(perCategoryNumpy)))
        tempResults.append(format(scipy.median(perCategoryNumpy)))                
        print("Minimum : {0:8.6f}".format(perCategoryNumpy.min()))
        tempResults.append(format(perCategoryNumpy.min()))
        print("Maximum : {0:8.6f}".format(perCategoryNumpy.max()))
        tempResults.append(format(perCategoryNumpy.max()))
        print("Std. deviation : {0:8.6f}".format(perCategoryNumpy.std()))
        tempResults.append(format(perCategoryNumpy.std()))
        print("Skewness : {0:8.6f}".format(skew(perCategoryNumpy)))
        tempResults.append(format(skew(perCategoryNumpy)))
        print("Kurtosis : {0:8.6f}".format(kurtosis(perCategoryNumpy)))
        tempResults.append(format(kurtosis(perCategoryNumpy))) 
        tempResults.append(cat)
        print "########################################"
        finalResults.append(tempResults)
        
    #create file name
    fileName = "statistics/EP_DescriptiveStatistics"+datetime.datetime.now().ctime()+".csv"
    #print fileName
    #write to csv
    out = csv.writer(open(fileName,"wb"), delimiter=';',quoting=csv.QUOTE_NONE)

    out.writerow(['Mean','Geometric mean','Harmonic mean','Median','Minimum','Maximum','Std. deviation','Skewness','Kurtosis','Category'])
    for results in finalResults:      
        out.writerow(results)
#main
def main():
    """
    Functions:
        1. getDescriptiveStatisticsCategory(document)
        2. getDescriptiveStatisticsEP()
    """ 
    print main.__doc__

    var = raw_input("Choose function to run: ")
        
    if var == "1":
        print getDescriptiveStatisticsCategory.__doc__
        getDescriptiveStatisticsCategory()
    elif var == "2":
        print getDescriptiveStatisticsEP.__doc__
        print getDescriptiveStatisticsEP()
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        
if __name__ == '__main__':    
    main()