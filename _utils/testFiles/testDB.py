import sys
sys.path.append("/home/jseva/SemanticVIRT/_utils/")
from ShevaDB import ShevaDB

#print ShevaDB().dbQuery("select * from analysis_f1 limit 100")
#print ShevaDB().dbQuery("select * from analysis_f1 limit 100")
print ShevaDB().getCategoryDepth("Regional")
print ShevaDB().getMainCat()