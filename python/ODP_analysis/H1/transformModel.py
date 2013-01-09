'''
Created on 8.1.2013.

@author: Jurica Seva

PhD Candidate 
Faculty of Organization and Informatics
University of Zagreb
'''
from python.ODP_analysis.utils import odpDatabase, odpDepth, parentChildDepth
from gensim import models, corpora
import sys
from python.ODP_analysis.utils.odpDatabase import errorMessage
from gensim.models.tfidfmodel import TfidfModel


def transformModel(modelType, inputModel="", dictionary=""):
    """
    Takes in TF IDF model and makes a transformation in to one of the following
    1 -> LSI model
    2 -> LDA model
    3 -> LogEntropy 
    
    based on value of modelType (first parameter)
    
    Default files -> test Newsgroup files
    corpusFiles/testNewsgroupsDictionary.dict
    corpusFiles/testNewsgroupsMmCorpus.mm
      
    """
    #check if using default dict or lcoation passed as parameter
    if dictionary == "":
        dictionary = corpora.Dictionary.load('corpusFiles/testNewsgroupsDictionary.dict')
        print dictionary
        #sys.exit(1)
    else:
        dictionary = corpora.Dictionary.load(dictionary)
        
    #use default stored model; mm format
    if inputModel == "":
        #inputModel = corpora.MmCorpus('corpusFiles/testNewsgroupsMmCorpus.mm')
        inputModel = TfidfModel.load("models/testNewsgroups.tfidf_model")
        print inputModel
    else:
        corpus = corpora.MmCorpus(inputModel)
        inputModel = models.TfidfModel(corpus)
        
        #sys.exit(1)        

    #create model handlers
    if modelType == "":
        print "Chose output model for selected input file: \n 1 -> LSI model\n 2 -> LDA model\n 3 -> LogEntropy model\n Pass it as the third parameter"
        sys.exit(1)    
    elif modelType == 1:
        model = models.LsiModel(inputModel,id2word=dictionary)
    elif type == 2:
        modelType = models.LdaModel(inputModel,id2word=dictionary)
    elif type == 3:
        modelType = models.LogEntropyModel(inputModel,id2word=dictionary)
    else:
        errorMessage("Something went wrong with the type identificator")
    
    return model

transformModel(modelType=1)