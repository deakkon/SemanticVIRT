#imports
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_recall_fscore_support
from itertools import izip


#Sheva import
#sys.path.append("/home/jseva/SemanticVIRT/_utils/")
#from ShevaCSV import ShevaCSV

class ShevaClassificationMetrics:

    #@profile
    def computeClassificationMetrics(self, testingOID, modelOID, similarity):
        """
        Get first item by similarity
        INPUT:
            testingOID -> list of original ID values from testing documents
            modelOID -> dictionary, original model ID at model row nr. 
            similarity -> similarity returned from testingDocuments vs modelDocuments
        OUTPUT: precision, recall, f1 masures for defined input
        """
        
        returnedCategoryID = []
        lookingFor = []
        for comparisonDocumentID, row in izip(testingOID, similarity):
            if len(row) != 0:
                maxTempSorted = row[0]
                lookingFor.append(comparisonDocumentID)
                returnedCategoryID.append(modelOID[str(maxTempSorted[0])])                  
            else:
                lookingFor.append(comparisonDocumentID)
                returnedCategoryID.append("0")

        if len(returnedCategoryID) > 0:
            precision, recall, F1, _ = precision_recall_fscore_support(lookingFor, returnedCategoryID, pos_label=None, average='weighted')
        else:
            precision = recall = F1 = 0
            
        return (precision,recall, F1)
        
        
    #@profile    
    def computeClassificationMetricsRelative(self, testingOID, modelOID, similarity):
        """
        Get items with sim == 1
        INPUT:w
            testingOID -> list of original ID values from testing documents
            modelOID -> dictionary, original model ID at model row nr. 
            similarity -> similarity returned from testingDocuments vs modelDocuments
        OUTPUT: precision, recall, f1 masures for defined input
        """
        returnedCategoryID = []
        lookingFor = []

        for comparisonDocumentID, row in izip(testingOID, similarity):
            foundMatch = False
            for item in row:
                if item[1] == 1.0 or modelOID[str(item[0])] == comparisonDocumentID:
                    lookingFor.append(comparisonDocumentID)
                    returnedCategoryID.append(modelOID[str(item[0])])
                    foundMatch = True
                    
            if foundMatch == False:
                lookingFor.append(comparisonDocumentID)
                returnedCategoryID.append("0")

        if len(returnedCategoryID) > 0:
            precision, recall, F1, _ = precision_recall_fscore_support(lookingFor, returnedCategoryID, pos_label=None, average='weighted')
        else:
            precision = recall = F1 = 0

        return (precision,recall, F1)
     
    def computeClassificationMetricsExclusive(self, testingOID, modelOID, similarity):
        """
        Get items with LookupID == modelID
        INPUT:
            testingOID -> list of original ID values from testing documents
            modelOID -> dictionary, original model ID at model row nr. 
            similarity -> similarity returned from testingDocuments vs modelDocuments
        OUTPUT: precision, recall, f1 masures for defined input
        """
        returnedCategoryID = []
        lookingFor = []

        for comparisonDocumentID, row in izip(testingOID, similarity):
            if len(row) != 0:
                
                granica = int(len(row)*0.1)
                if granica == 0:
                    granica = 1
                
                foundMatch = False
                
                for temp in row[:granica]:
                    #modelRowIDItem = modelOID.hget("bucket:" + str(int(temp[0]/100)), temp[0])
                    modelRowIDItem = modelOID[str(temp[0])]
                    #print "temp[0]: ",type(temp[0]),"\tcomparisonDocumentID:",type(comparisonDocumentID),"\tmodelOID[str(temp[0])]",type(modelOID[str(temp[0])])
                    if modelRowIDItem ==  comparisonDocumentID:
                        lookingFor.append(comparisonDocumentID)
                        returnedCategoryID.append(modelRowIDItem)
                        foundMatch = True
                        
                if foundMatch == False:
                    lookingFor.append(comparisonDocumentID)
                    returnedCategoryID.append("0")
            else:
                lookingFor.append(comparisonDocumentID)
                returnedCategoryID.append("0")

        if len(returnedCategoryID) > 0:
            precision, recall, F1, _ = precision_recall_fscore_support(lookingFor, returnedCategoryID, pos_label=None, average='weighted')
        else:
            precision = recall = F1 = 0

        return (precision,recall, F1)

