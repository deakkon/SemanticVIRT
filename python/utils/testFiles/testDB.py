from sys import path
path.append("/home/jseva/SemanticVIRT/python/utils/")
from ShevaDB import ShevaDB as baza

b = baza()

print b.dbQuery("select * from analysis_f1")