'''
Created on 17.12.2012.

@author: Jurica

Testing two approaches in calculating ODP's depth level for further analysis

1) parsin' the field Topic from dmoz_categories, split by delimiter "/"
2) using fatherid in reverse order (bottom up) vs bottom down; Dictionary data structure

'''
import sys
from odpDatabase import *

def parentChildDepth(a, b):
    """
    Returns all categories, without parend-child relationship, in between two levels
    a has to be smaller or equall then b
    """
    if a > b:
        errorMessage("First parameter has to be smaller than the second")
        sys.exit()
    else: 
        con = dbConnect()
        sql = "select count(*) from dmoz_categories where categoryDepth >= '%s' and categoryDepth <= '%s'" % (a,b)
        #print sql
        res = dbQuery(con, sql)
        """
        print res
        for i in res:
            print i
        """
        return res
        
        
def returnParentsNumber(node):
    """
    Returns number of parent nodes of the passed parameter
    node -> catid, numerical number of category 
    """
    if node == "":
        errorMessage("Passed parameter is empty. Relaunch.")
        sys.exit()
    else:         
        depth = -1
        level = 0
        while depth != 0 and node != 0:        
            con = dbConnect()            
            sqlCount = "select fatherid from dmoz_categories where catid = '%s'" %node
            res = dbQuery(con, sqlCount)
            depth = len(res)
            node = res[0]
            level += 1
            print "#####################################################################"
            print "sql: ",sqlCount
            print "depth", depth
            print "node", node
            print "level", level                    
        print "Number of parents = ", depth
        
            
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
        sql = "select * from dmoz_categories where Topic like '%/"+str(topic)+"/%' and categoryDepth >= '"+str(a)+"' and categoryDepth <= '"+str(b)+"'"    
        con = dbConnect()
        res = dbQuery(con, sql)
        #print res.rowcount
        return res


#parentChildDepth(2, 4)
#returnParentsNumber(6277481)
print returnChildrenNodes("Arts",2,7)