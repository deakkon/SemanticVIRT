'''
Created on 8.1.2013.

@author: Jurica Seva

PhD Candidate 
Faculty of Organization and Informatics
University of Zagreb
'''
def transformModel(inputModel, dictionary ,type = 0):    
    #create model handlers
    if type == 0:
        print "Chose output model for selected input file: \n 1 -> LSI model\n 2 -> LDA model\n 3 -> LogEntropy model\n Pass it as the third parameter"    
    elif type == 1:
        model = models.LsiModel(inputModel)
    elif type == 2:
        model = models.LsiModel(inputModel)
    elif type == 3:
        model = models.LsiModel(inputModel)
    