#improt
import csv
import sys

#Sheva import
#sys.path.append("/home/jseva/SemanticVIRT/_utils/")
#from ShevaDB import ShevaDB

class ShevaCSV:
    
    def __init__(self):
        print "ShevaCSV created"
        
    def __del__(self):
        print 'ShevaCSV destroyed'
        
    def write2CSV(self, fileName, path):
        """
        Write to csv
        data: type list
        fileName: string
        path: where to save
        """
        self.checkIfList(self)
        writeLabels = []
        for row in self.data:
            for i in row:
                if i != "" or i.lower() not in string.letters.lower():
                    writeLabels.append(i.lower())

    #def getCategoryLabel(self, labels,fileName, dataset):
    def writeDatasetLabel(self, labels,fileName, dataset):
        """
        categoryLabels -> list of labels to write to disk
        fileName -> file to save labels returned by the query
        """
        #lables array for level, for % of accesed rows
        writeLabels = []
    
        #file to save data to 
        fileName = "testData/%s/labels/%s.csv" %(dataset,fileName)
        out = csv.writer(open(fileName,"w"), delimiter=',',quoting=csv.QUOTE_ALL)
    
        for row in categoryLabels:
            for i in row:            
                if i != "" or i.lower() not in string.letters.lower():
                    writeLabels.append(i.lower())
        out.writerow(writeLabels)

    #def getCategoryListLevel(self, catID, fileName, path):
    def writeOriginalID(self, catID, fileName, path):
        """
        catID: original cadID while creating data
        fileName: fileName for saving
        path: path to store csv files
        """
        #create csv
        resultsSavePath = "%sorigCATID/%s.csv" %(path,fileName)
        originalCSV  = open(resultsSavePath, "wb")
        csvResults = csv.writer(summaryFile, delimiter=',',quoting=csv.QUOTE_ALL)
        csvResults.writerow(('model row','CATID'))
    
        for i in list(enumerate(catID)):
            if str(i[1]) == "e":
                print "Es in the house:\t",i[0],"\t",i[1]
            else:
                csvResults.writerow((i[0],i[1]))
        summaryFile.close()
        
    def createCSV(self, savePath, content):
        with open(savePath, "wb") as the_file:
            csv.register_dialect("custom", delimiter=",", skipinitialspace=True)
            writer = csv.writer(the_file, dialect="custom")
            for item in content:
                writer.writerow(item)
        
    def getCategoryListLevel(self, data, fileName, path):
        """
        catID: original cadID while creating data
        fileName: fileName for saving
        dataset: % model of data
        """
        #create csv
        resultsSavePath = "%soriginalID/%s.csv" %(path,fileName)
        summaryFile  = open(resultsSavePath, "wb")
        csvResults = csv.writer(summaryFile, delimiter=',',quoting=csv.QUOTE_ALL)
        csvResults.writerow(('modelRowNumber','original_ID'))
    
        for i in list(enumerate(data)):
            #print i
            if str(i[1]) == "e":
                print "Es in the house:\t",i[0],"\t",i[1]
            else:
                csvResults.writerow((i[0],i[1]))
        
        summaryFile.close()
        
    def getOriginalRowFromModel(self, modelRow, modelDocument):
        originalRow = "Empty"
        #open csv
        f = open(modelDocument, "rb")
        reader = csv.reader(f)
    
        #default
        for row in reader:
            #print row[0]
            if row[0] == str(modelRow):
                originalRow = row[1]
                f.close()
                return originalRow
        f.close()
        
    def getIDfromModel(self, fileName):
        """
        RETURN: unique ID values from filename
        """
        data = []
        r = csv.reader(open(fileName))
        headers = r.next()
        for fields in r:
            if fields[1] not in data:
                data.append(fields[1])
        return data
    
    #@profile
    def getModelCSV(self, modelFileName):
        """
        RETURN: all (modelRow,originalID) from filename
        """
        #csv original id from model
        f = open(modelFileName, "rb")
        header = ["modelRowNumber","original_ID"]
        readerTemp = csv.DictReader(f,header)
        readerTemp.next()
        reader = {row['modelRowNumber']:row['original_ID'] for row in readerTemp}
        f.close()
        return reader
    """
    def getModelCSV_REDIS(self,modelFileName):
        redisServer = self.shevaDB.createREDIS()
        f = open(modelFileName, "rb")
        header = ["modelRowNumber","original_ID"]
        readerTemp = csv.DictReader(f,header)
        readerTemp.next()        
        for item in readerTemp:
            #print item
            #print item['modelRowNumber']
            redisServer.hset("bucket:" + str(int(int(item['modelRowNumber'])/100)), item['modelRowNumber'] ,item['original_ID'])
        f.close()
        return redisServer
    """
        