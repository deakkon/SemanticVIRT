import  matplotlib, sys, numpy, datetime
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from python.utils.odpStatistics import getCatInfo
from python.utils.databaseODP import dbQuery

#functions        
def getGraphCategories(type=""):
    """
    Get basic graphs for table categories
    type=   1 -> histogram
            2 -> lineGraph
                
    """
    if  type == "":
        #print getGraphCategories.__doc__
        sys.exit("No parameters passed. Look above for instructions")
    else:
        categories = getCatInfo()
        allValues = []
        allValuesMaxDepth = 0
        
        #histogram    
        if type == "1":
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
                fn = "histograms/"+cat+"_CAT_"+datetime.datetime.now().ctime()
                #save graph        
                plt.savefig(fn)
        
        #line graph
        elif type == "2":
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
                            
                #list of list -> y axis in plot
                allValues.append(perCategory)
                
                #max depth -> x axis in plot
                if allValuesMaxDepth < maxDebthRS[0]:
                    allValuesMaxDepth = maxDebthRS[0]
            
            #plot line graphs
            plt.figure()
            x_series = range(allValuesMaxDepth)
            #print x_series
            
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
            #plt.ylim(0, 20000) 
            plt.legend(loc="upper right")
            fileName = "lineGraph/"+datetime.datetime.now().ctime()+"LineGraph.png"
            plt.savefig(fileName)
    

def getGraphExternalPages(type=""):
    """
    Get basic graphs for table externalpages
    type=   1 -> histogram
            2 -> lineGraph
                
    """
    if  type == "":
        #print getGraphCategories.__doc__
        sys.exit("No parameters passed. Look above for instructions.")
    else:
        categories = getCatInfo()
        allValues = []
        allValuesMaxDepth = 0
        
        #histogram    
        if type == "1":
            for cat in categories:
                #variables, specific for cat
                perCategory = []
                sqlMaxDepth = "select max(categoryDepth) from dmoz_categories where Topic like '%/"+str(cat)+"/%' and filterOut = 0"
                #query results
                maxDebthRS = dbQuery(sqlMaxDepth)
                #for each depth level
                for depth in range(1,maxDebthRS[0]):
                    #print depth                    
                    sqlDepth = "select count(*) from dmoz_externalpages where catid in (select catid from dmoz_categories where Topic like '%/"+str(cat)+"/%' and categoryDepth="+str(depth)+")"                    
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
                fn = "histograms/"+cat+"_EP_"+datetime.datetime.now().ctime()
                #save graph        
                plt.savefig(fn)
        
        #line graph
        elif type == "2":
            for cat in categories:
                #variables, specific for cat
                perCategory = []
                sqlMaxDepth = "select max(categoryDepth) from dmoz_categories where Topic like '%/"+str(cat)+"/%' and filterOut = 0"
                #query results
                maxDebthRS = dbQuery(sqlMaxDepth)
                #for each depth level
                for depth in range(1,maxDebthRS[0]):
                    #print depth
                    sqlDepth = "select count(*) from dmoz_externalpages where catid in (select catid from dmoz_categories where Topic like '%/"+str(cat)+"/%' and categoryDepth="+str(depth)+")"
                    debthRowCount = dbQuery(sqlDepth)
                    #print debthRowCount[0]
                    #print sqlDepth
                    perCategory.append(debthRowCount[0])
                            
                #list of list -> y axis in plot
                allValues.append(perCategory)
                
                #max depth -> x axis in plot
                if allValuesMaxDepth < maxDebthRS[0]:
                    allValuesMaxDepth = maxDebthRS[0]
            
            #plot line graphs
            plt.figure()
            x_series = range(allValuesMaxDepth)
            #print x_series
            
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
            #plt.ylim(0, 20000) 
            plt.legend(loc="upper right")
            fileName = "lineGraph/EP_"+datetime.datetime.now().ctime()+"LineGraph.png"
            plt.savefig(fileName)
    
    
#main
def main():
    """
    Functions:
        1. getGraphCategories()
        2. getGraphExternalPages()
    """ 
    print main.__doc__

    var = raw_input("Choose function to run: ")
        
    if var == "1":
        print getGraphCategories.__doc__
        var1 = raw_input("Input graph type: ")
        getGraphCategories(var1)
    elif var == "2":
        print getGraphExternalPages.__doc__
        var1 = raw_input("Input graph type: ")
        getGraphExternalPages(var1)        
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        
if __name__ == '__main__':    
    main()