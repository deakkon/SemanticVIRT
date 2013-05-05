import sys
sys.path.append("/home/jseva/SemanticVIRT/_utils/")
sys.path.append("/home/jseva/SemanticVIRT/classification(H1)/")

from ShevaDB import ShevaDB
from ShevaTPF import ShevaTPF
from ShevaUtils import ShevaUtils
from ShevaVect import ShevaVect
from ShevaLevelModels import createDataLevel

rootDirectory = raw_input("Input root directory to store files (keyboard input): ")

dataModel = createDataLevel(2,rootDirectory)
print dataModel.GROUPTYPE
print dataModel.percentageList
print dataModel.rootDir
print dataModel.createData("Regional")
