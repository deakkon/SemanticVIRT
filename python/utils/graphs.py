import  matplotlib, sys, numpy, datetime
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from python.utils.odpStatistics import getCatInfo
from python.utils.databaseODP import dbQuery

def getHistogram():
    """
    Create histograms, depicting 
    """  
    categories = getCatInfo()

    
    for cat in categories:
        #variables, specific for cat
        perCategory = []
        sqlMaxDepth = "select max(categoryDepth) from dmoz_categories where Topic like '%/"+str(cat)+"/%' and filterOut = 0"
        #query results
        maxDebthRS = dbQuery(sqlMaxDepth)
        #for each depth level
        for depth in range(1,maxDebthRS[0]):
            #print depth
            sqlDepth = "select count(*) from dmoz_categories where Topic like '%/"+str(cat)+"/%' and filterOut = 0 and categoryDepth="+str(depth)
            debthRowCount = dbQuery(sqlDepth)
            #print debthRowCount[0]
            #print sqlDepth
            perCategory.append(debthRowCount[0])
            
        perCategoryNumpy = numpy.asarray([perCategory[x] for x in range(len(perCategory))])
        #prepare data
        alphab = range(len(perCategoryNumpy))
        frequencies = perCategoryNumpy
        #print lengths   
        print alphab, "    ",frequencies
        
        pos = numpy.arange(len(alphab))
        width = 1.0     # gives histogram aspect to the bar diagram
        
        ax = plt.axes()
        ax.set_xticks(pos + (width / 2))
        ax.set_xticklabels(alphab)
        plt.bar(pos, frequencies, width, color='r')
        #filename
        fn = "histograms/"+cat+"_"+datetime.datetime.now().ctime()
        #save graph        
        plt.savefig(fn)        
        
def getLineGraph():
    
    categories = getCatInfo()
    allValues = []
    allValuesMaxDepth = 0

    
    for cat in categories:
        #variables, specific for cat
        perCategory = []
        sqlMaxDepth = "select max(categoryDepth) from dmoz_categories where Topic like '%/"+str(cat)+"/%' and filterOut = 0"
        #query results
        maxDebthRS = dbQuery(sqlMaxDepth)
        #for each depth level
        for depth in range(1,maxDebthRS[0]):
            #print depth
            sqlDepth = "select count(*) from dmoz_categories where Topic like '%/"+str(cat)+"/%' and filterOut = 0 and categoryDepth="+str(depth)
            debthRowCount = dbQuery(sqlDepth)
            #print debthRowCount[0]
            #print sqlDepth
            perCategory.append(debthRowCount[0])
            if debthRowCount[0] > 50000:
                print cat,"        ",depth
                
        
        #list of list -> y axis in plot
        allValues.append(perCategory)
        
        
        #max depth -> x axis in plot
        if allValuesMaxDepth < maxDebthRS[0]:
            allValuesMaxDepth = maxDebthRS[0]
    
    #plot line graphs
    plt.figure()
    x_series = range(allValuesMaxDepth)
    print x_series
    
    #iterator to go through categories, for labels, categories[i]
    i = 0
    
    #same dimensions
    for topic in allValues:
        while len(topic)<allValuesMaxDepth:
            topic.append(0)        
        plt.plot(x_series, topic, label=categories[i])
        i += 1
    
    plt.xlabel("Depth level")
    plt.ylabel("Number of labels")
    plt.title("Number of labels per depth level")
    
    plt.legend(loc="upper right")
    plt.savefig("example.png")
    
#main
def main():
    """
    Functions:
        1. getHistogram()
        2. getLineGraph()
    """ 
    print main.__doc__

    var = raw_input("Choose function to run: ")
        
    if var == "1":
        print getHistogram.__doc__
        getHistogram()
    elif var == "2":
        print getLineGraph.__doc__
        getLineGraph()        
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        
if __name__ == '__main__':    
    main()