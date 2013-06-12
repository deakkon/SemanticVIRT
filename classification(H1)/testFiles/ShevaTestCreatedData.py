import sys
import gensim
from gensim import corpora, models
#USER DEFINED MODULES
sys.path.append("/home/jseva/SemanticVIRT/_utils/")
from ShevaDB import ShevaDB

class TestCreatedData:
    
    def __init__(self,rootDir):
        self.root = rootDir
        self.GROUPTYPE = ["CATID","FATHERID","GENERAL"]
        self.percentageList = [25, 50, 75, 100]
        self.shevaDB = ShevaDB()
        
    def checkCreatedModels(self,category):
        ranger = self.shevaDB.getCategoryDepth(category)
        var = ""
        for group in self.GROUPTYPE:
            for percentageItem in self.percentageList:
                for indeks in ranger:
                    fileNameAll = "%s_%s_1_%s" %(str(percentageItem),category,str(indeks))
                    fileNameLevel = "%s_%s_%s" %(str(percentageItem),category,str(indeks))
                    fileNameSingleAll = "%s_%s_%s_single" %(str(percentageItem),category,str(indeks))
                    
                    dictDirLevel = "../%s/%s/%s/dict/%s.dict" %(self.root,group,str(percentageItem),fileNameLevel)
                    dictDirRange = "../%s/%s/%s/dict/%s.dict" %(self.root,group,str(percentageItem),fileNameAll)
                    
                    dictionaryLevel = corpora.Dictionary.load(dictDirLevel)
                    dictionaryRange = corpora.Dictionary.load(dictDirRange)
                    """
                    print "Level dict %s: %s" %(fileNameLevel, dictionaryLevel)
                    print "Range dict %s: %s" %(fileNameAll, dictionaryRange)
                    """
                    var += "Level dict %s: %s\n" %(fileNameLevel, dictionaryLevel)
                    var += "Range dict %s: %s\n" %(fileNameAll, dictionaryRange)
                    
                    corpusDirLevel = "../%s/%s/%s/corpus/%s.mm" %(self.root,group,str(percentageItem),fileNameLevel)
                    corpusDirRange = "../%s/%s/%s/corpus/%s.mm" %(self.root,group,str(percentageItem),fileNameAll)
                            
                    corpusLevel = corpora.MmCorpus(corpusDirLevel)
                    corpusRange = corpora.MmCorpus(corpusDirRange)
                    """
                    print "Level corpus %s: %s" %(fileNameLevel, corpusLevel)
                    print "Range corpus %s: %s" %(fileNameAll, corpusRange)
                    """
                    var += "Level corpus %s: %s\n" %(fileNameLevel, corpusLevel)
                    var += "Range corpus %s: %s\n" %(fileNameAll, corpusRange)
                    var += "###################################################################\n"
        return var
                    

                    
    def runCheck(self):
        inputs = self.shevaDB.getMainCat()
        var = ""
        for index in inputs:
            var += self.checkCreatedModels(index)

        f = open('analizaDoc2Dict.txt', 'w')
        f.write( var)
        f.close()
            
var = raw_input("Root dir: ")
tcd = TestCreatedData(var)
tcd.runCheck()