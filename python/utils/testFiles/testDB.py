from db import ShevaDB as baza

b = baza()

print b.dbQuery("select * from analysis_f1")