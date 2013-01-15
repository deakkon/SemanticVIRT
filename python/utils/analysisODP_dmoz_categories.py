'''
Created on 17.12.2012.

@author: Jurica

Testing two approaches in calculating ODP's depth level for further analysis

1) parsin' the field Topic from dmoz_categories, split by delimiter "/"
2) using fatherid in reverse order (bottom up) vs bottom down; Dictionary data structure

'''
#imports
import sys
from databaseODP import dbQuery, errorMessage

#functions

def parentChildDepthNumber_dmoz_categories(a,b):
    """
    Returns number of categories, disregarding parend-child relationship, in between two levels, with a <= b
    """
    res = ""
    if a > b:
        errorMessage("First parameter has to be smaller than the second")
        sys.exit(1)
    else: 
        sql = "select count(*) from dmoz_categories where categoryDepth >= '%s' and categoryDepth <= '%s' and filterOut != '-1'" % (a,b)
        res = dbQuery(sql)
    return res      
        
def parentNodesNumber_dmoz_categories(nodeCatId):
    """
    Input parameters: node ->  catid of node 
        
    Returns list of parents of node 
    """
    #variables
    parentNodes = []
    
    if nodeCatId == "":
        errorMessage("Passed parameter is empty. Relaunch.")
    else:         
        depth = -1
        level = 0
        while depth != 0 and nodeCatId != 1:              
            sqlCount = "select fatherid from dmoz_categories where catid = '%s' and filterOut != '-1'" %nodeCatId
            res = dbQuery(sqlCount)
            depth = len(res)
            nodeCatId = res[0]
            parentNodes.append(nodeCatId)
            level += 1
            """
            print "#####################################################################"
            print "sql: ",sqlCount
            print "depth", depth
            print "node", nodeCatId
            print "level", level
            """                  
            print "Number of parents = ", depth
        return parentNodes
        
def parentNodesList_dmoz_categories(topicID):
    """
    Input parameters: node ->  catid of node 
    Returns python list of catid's who have the same parents as starting node, from level n to level 1 (TOP category)  
    """
   
    if topicID == "":
        errorMessage("Passed parameter is empty. Relaunch.")
    else:         
        childrenNodes = []
        depth = -1
        level = 0
        while depth != 0 and topicID > 1:             
            #get fatherid untill you get to root
            #print topicID
            sqlCount = "select fatherid,categoryDepth from dmoz_categories where catid = '%s' and filterOut != '-1'" %topicID
            #print sqlCount
            res = dbQuery(sqlCount)
            depth = len(res)
            categoryDepth = res[1]
            topicID = res[0]
            level += 1
            
            #get all categories where father = fatherid (node)
            sqlChildren = "select catid from dmoz_categories where fatherid = '%s'  and filterOut != '-1'" %topicID
            #print sqlChildren
            resChildren = dbQuery(sqlChildren)
            #print "lista:",list(resChildren)
            #print "ne lista", resChildren
            for child in resChildren:
                #print "bez polja ", child
                #print "sa poljem ", child[0]
                if categoryDepth > 1:
                    childrenNodes.append(child)
            #print "children nodes ", childrenNodes
        return childrenNodes
            
def returnChildrenNodes(topic, a, b):
    """
    Nodes between a and b belonging to a specific topic (based on the original category path)
    Topics:
    "Title"
    "Arts"
    "Business"
    "Computers"
    "Games"
    "Health"
    "Home"
    "Kids_and_Teens"
    "News"
    "Recreation"
    "Reference"
    "Regional"
    "Science"
    "Shopping"
    "Society"
    "Sports"
    """
    if a > b:
        errorMessage("First parameter has to be smaller than the second")
        sys.exit()
    else:     
        sql = "select * from dmoz_categories where Topic like '%/"+str(topic)+"/%' and categoryDepth >= '"+str(a)+"' and categoryDepth <= '"+str(b)+"' and filterOut != '-1'"    
        res = dbQuery(sql)
        #print res.rowcount
        return res

def depthTopicUpdate():
    """
    Calculates level od depthnes for specific category, in dmoz_categories, based on delimiter "/"
    e.g. a/b/c/d/e -> e is on level 4 with a being root (0) level
    updates categoryDepth with depth level information
    """
    #function variables
    seq = []
    
    #db
    sql = "select id,Topic, (length(Topic)-length(replace(Topic,'/','')))/length('/') as nR, fatherid, categoryDepth FROM dmoz_categories n where filterOut=0"
    resultRows = dbQuery(sql)
    #print resultRows

    for row in resultRows:
        seq.append([int(row[2]),int(row[0])])    

        """                         
        print row, "    ",str(row).count("/")
        print row[0],"    ",row[1],"                                                                ",int(i[2])
        """
        
        sql = "update dmoz_categories set categoryDepth = '%s' WHERE id = '%s' and filterOut != '-1'" % (int(row[2]),int(row[0]))
        dbQuery(sql)

def main():
    """
    Functions:
           1: parentChildDepth_dmoz_categories((a, b)
           2: parentNodesNumber_dmoz_categories(nodeCatId)
           3: parentNodesNumber_dmoz_categories(nodeCatId)
           4: returnChildrenNodes(topic, a, b)
           5: depthTopicUpdate()
           anything else for exit    
    """ 
    print main.__doc__
    
    var = raw_input("Choose a function: ")
        
    if var == "1":        
        print parentChildDepthNumber_dmoz_categories.__doc__
        var1 = raw_input("Enter first depth: ")
        var2 = raw_input("Enter second depth: ")
        print parentChildDepthNumber_dmoz_categories(var1, var2)
    elif var == "2":
        print parentNodesNumber_dmoz_categories.__doc__
        var1 = raw_input("Enter node category id (catID value): ")
        print parentNodesNumber_dmoz_categories(var1)
    elif var == "3":
        print parentNodesList_dmoz_categories.__doc__
        var1 = raw_input("Enter node category id (catID value): ")
        print parentNodesList_dmoz_categories(var1)    
    elif var == "4":
        print returnChildrenNodes.__doc__
        var1 = raw_input("Enter node topic name (Topic field value): ")
        var2 = raw_input("Enter first depth: ")
        var3 = raw_input("Enter second depth: ")        
        print returnChildrenNodes(var1,var2,var3)
    elif var == "5":
        print depthTopicUpdate.__doc__    
        print depthTopicUpdate()        
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
        

if __name__ == '__main__':    
    main()
