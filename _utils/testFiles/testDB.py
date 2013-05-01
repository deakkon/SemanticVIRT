import sys
sys.path.append("/home/jseva/SemanticVIRT/_utils/")
#sys.path.insert(0, '~/SemanticVIRT/_utils')
#from ShevaDB import ShevaDB as baza
from ShevaDB import ShevaDB

print ShevaDB().dbQuery("select * from analysis_f1 limit 100")