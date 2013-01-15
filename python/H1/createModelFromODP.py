'''
Created on 9.1.2013.

@author: Jurica Seva

PhD Candidate 
Faculty of Organization and Informatics
University of Zagreb
'''
#imports
import logging
from python.utils.databaseODP import *
from python.H1.createVectorModel import *
from python.H1.calculateSimilarity import *

#logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#functions
def createTFIDFfromODP_dmoz_descriptions(topic="",depthStart="", depthEnd=""):
    #if any of the arguments emty exit
    if topic == "":
        errorMessage("First paramter is missing")    
    if depthStart == "": 
        errorMessage("Second paramter is missing")    
    if depthEnd == "":
        errorMessage("Third paramter is missing")
    
    #data from db
    sql = "select * from dmoz_categories where Topic like '%/"+str(topic)+"/%' and categoryDepth >= '"+str(depthStart)+"' and categoryDepth <= '"+str(depthEnd)+"'"
    res = dbQuery(sql)
    
    #create dynamic file names
    saveFileName = str(topic)+"_"+str(depthStart)+"_"+str(depthEnd)    
    #print saveFileCorpus, "    ",saveFileModel
    
    #create corpora and model from db query results
    createCorpusAndVectorModel(res,fileName=saveFileName)
            
createTFIDFfromODP_dmoz_descriptions("Arts",1,3)