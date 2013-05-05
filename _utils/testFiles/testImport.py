import sys
sys.path.append("/home/jseva/SemanticVIRT/_utils/")
import ShevaDB 

print ShevaDB.ShevaDB().dbQuery("select * from analysis_f1 limit 100")