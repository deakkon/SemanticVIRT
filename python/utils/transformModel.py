'''
Created on 8.1.2013.

@author: Jurica Seva

PhD Candidate 
Faculty of Organization and Informatics
University of Zagreb
'''

from gensim import models, corpora
import sys
from python.utils.databaseODP import errorMessage
from gensim.models.tfidfmodel import TfidfModel


def transformModel(transformSource, modelType, inputModel="", dictionary=""):
    """
    Input parameters: modelType, inputModel="", dictionary=""
    
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
        dictionary = corpora.Dictionary.load('dictionaries/testNewsgroupsDictionary.dict')
        print dictionary
        #sys.exit(1)
    else:
        fileName = 'dictionaries/'+str(dictionary)
        dictionary = corpora.Dictionary.load(fileName)
        
    #use default stored model; mm format
    if inputModel == "":
        inputModel = TfidfModel.load("models/testNewsgroups.tfidf_model")
        #print inputModel
    else:
        fileName = 'models/'+str(inputModel)
        corpus = corpora.MmCorpus(inputModel)
        inputModel = models.TfidfModel(corpus)
        
        #sys.exit(1)        

    #create model handlers
    if modelType == "":
        print "Chose output model for selected input file: \n 1 -> LSI model\n 2 -> LDA model\n 3 -> LogEntropy model\n Pass it as the third parameter"
        sys.exit(1)    
    elif modelType == 1:
        model = models.LsiModel(inputModel,id2word=dictionary)
    elif modelType == 2:
        model = models.LdaModel(inputModel,id2word=dictionary)
    elif type == 3:
        model = models.LogEntropyModel(inputModel,id2word=dictionary)
    else:
        errorMessage("Something went wrong with the type identificator")
    
    return model

#transformModel(modelType=1)
def main():
    """
    Functions:
        1.vectorizeDocument(document)
        2.createCorpusAndVectorModel(documents, outputFormat=1, modelFormat=1, fileName ="")
    """ 
    print main.__doc__

    var = raw_input("Choose function to run: ")
        
    if var == "1":
        print transformModel.__doc__
        var1 = "Input text to vectorize"
        print transformModel(var1)    
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
    sys.exit(0)
        
if __name__ == '__main__':    
    main()