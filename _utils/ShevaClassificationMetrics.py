#imports
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

class ShevaClassificationMetrics:

    def computeClassificationMetrics(self, testingOID, modelOID, similarity):
        """
        INPUT:
            testingOID -> list of original ID values from testing documents
            modelOID -> dictionary, original model ID at model row nr. 
            similarity -> similarity returned from testingDocuments vs modelDocuments
        OUTPUT:
        """
        returnedCategoryID = []
        lookingFor = []
        
        for comparisonDocumentID, row in zip(testingOID, similarity):
            for item in row:
                lookingFor.append(str(comparisonDocumentID).strip())
                returnedCategoryID.append(str(modelOID[str(item[0])]).strip())

        if len(lookingFor) == 2 or len(returnedCategoryID) == 2:
            print "Test ID length:",len(lookingFor),"\t\t","Returned Model ID length:",len(returnedCategoryID)
            #,"\n",lookingFor,"\n",returnedCategoryID

        if len(returnedCategoryID) > 0:
            precision = precision_score(lookingFor, returnedCategoryID, pos_label=None)
            recall = recall_score(lookingFor, returnedCategoryID, pos_label=None)
            F1 = f1_score(lookingFor, returnedCategoryID, pos_label=None)
        else:
            precision = recall = F1 = 0
            
        return (precision,recall, F1)
    
    def computeClassificationMetricsRelative(self, testingOID, modelOID, similarity):
        """
        INPUT:
            testingOID -> list of original ID values from testing documents
            modelOID -> dictionary, original model ID at model row nr. 
            similarity -> similarity returned from testingDocuments vs modelDocuments
        OUTPUT:
        """
        returnedCategoryID = []
        lookingFor = []

        for comparisonDocumentID, row in zip(testingOID, similarity):
            for item in row:
                if (int(modelOID[str(item[0])]) ==  int(comparisonDocumentID)) or (item[1] == 1.0):
                    lookingFor.append(str(comparisonDocumentID).strip())
                    returnedCategoryID.append(str(modelOID[str(item[0])]).strip())

        if len(lookingFor) == 2 or len(returnedCategoryID) == 2:
            print "Test ID length:",len(lookingFor),"\t\t","Returned Model ID length:",len(returnedCategoryID)
            #,"\n",lookingFor,"\n",returnedCategoryID
        
        
        if len(returnedCategoryID) > 0:
            precision = precision_score(lookingFor, returnedCategoryID, pos_label=None)
            recall = recall_score(lookingFor, returnedCategoryID, pos_label=None)
            F1 = f1_score(lookingFor, returnedCategoryID, pos_label=None)
        else:
            precision = recall = F1 = 0

        return (precision,recall, F1)
    
    def computeClassificationMetricsExclusive(self, testingOID, modelOID, similarity):
        """
        INPUT:
            testingOID -> list of original ID values from testing documents
            modelOID -> dictionary, original model ID at model row nr. 
            similarity -> similarity returned from testingDocuments vs modelDocuments
        OUTPUT:
        """
        returnedCategoryID = []
        lookingFor = []

        for comparisonDocumentID, row in zip(testingOID, similarity):
            for item in row:
                if (int(modelOID[str(item[0])]) ==  int(comparisonDocumentID)) and (item[1] == 1.0):
                    lookingFor.append(str(comparisonDocumentID).strip())
                    returnedCategoryID.append(str(modelOID[str(item[0])]).strip())
        
        if len(lookingFor) == 2 or len(returnedCategoryID) == 2:
            print "Test ID length:",len(lookingFor),"\t\t","Returned Model ID length:",len(returnedCategoryID)
            #,"\n",lookingFor,"\n",returnedCategoryID
        
        if len(returnedCategoryID) > 0:
            precision = precision_score(lookingFor, returnedCategoryID, pos_label=None)
            recall = recall_score(lookingFor, returnedCategoryID, pos_label=None)
            F1 = f1_score(lookingFor, returnedCategoryID, pos_label=None)
        else:
            precision = recall = F1 = 0
            
        return (precision,recall, F1)  