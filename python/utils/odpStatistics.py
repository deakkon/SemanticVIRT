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
import logging, sys, csv, numpy, scipy, matplotlib
from scipy import stats
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
        
def getDescriptiveStatistics():
    """
    Basic statistics for each category, level based:
        1. Mean
        2. Min
        3. Max
        4. Variance
        5. Std. variation
        6. Median
    """
    #redirect output
    sys.stdout = open('descStat1.txt', 'w')
                 
    #variables
    categories = getCatInfo()
    fpr = open('basicStats.txt', 'w')
    
    for cat in categories:
        #variables, specific for cat
        perCategory = []
        sqlMaxDepth = "select max(categoryDepth) from dmoz_categories where Topic like '%/"+str(cat)+"/%' and filterOut = 0"
        #query results
        maxDebthRS = dbQuery(sqlMaxDepth)
        #for each depth level
        for depth in range(1,maxDebthRS[0]):
            sqlDepth = "select count(*) from dmoz_categories where Topic like '%/"+str(cat)+"/%' and filterOut = 0 and categoryDepth="+str(depth)
            debthRowCount = dbQuery(sqlDepth)
            perCategory.append(debthRowCount[0])
        perCategoryNumpy = numpy.asarray([perCategory[x] for x in range(1,len(perCategory))])
        print perCategoryNumpy
       
        """
        n, min_max, mean, var, skew, kurt = stats.describe(perCategory)
        print "Category: ", cat
        print("Number of elements: {0:d}".format(n))        
        print("Minimum: {0:8.6f} Maximum: {1:8.6f}".format(min_max[0], min_max[1]))
        print("Mean: {0:8.6f}".format(mean))
        print("Variance: {0:8.6f}".format(var))        
        print("Skew : {0:8.6f}".format(skew))
        print("Kurtosis: {0:8.6f}".format(kurt))        
        print "########################################"
        """
        print("Mean : {0:8.6f}".format(perCategoryNumpy.mean()))
        print("Minimum : {0:8.6f}".format(perCategoryNumpy.min()))
        print("Maximum : {0:8.6f}".format(perCategoryNumpy.max()))
        print("Variance : {0:8.6f}".format(perCategoryNumpy.var()))
        print("Std. deviation : {0:8.6f}".format(perCategoryNumpy.std()))
        print("Median : {0:8.6f}".format(scipy.median(perCategoryNumpy)))
        print "########################################"
        
def createHistogram():
    pass



#main
def main():
    """
    Functions:
        1. getCatInfo(document)
        2. getDescriptiveStatistics()
    """ 
    print main.__doc__

    var = raw_input("Choose function to run: ")
        
    if var == "1":
        print getCatInfo.__doc__
        getCatInfo()
    elif var == "2":
        print getDescriptiveStatistics.__doc__
        print getDescriptiveStatistics()
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        
if __name__ == '__main__':    
    main()