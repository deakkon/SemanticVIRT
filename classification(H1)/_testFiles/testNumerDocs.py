import sys
sys.path.append("/home/jseva/SemanticVIRT/_utils/")
from ShevaDB import ShevaDB


main = ShevaDB().getMainCat()


for m in main: 
    #getCats = "select catid from dmoz_categories where dmoz_categories.mainCategory = %s" %(m)
    sqlCont = "select count(*) from dmoz_externalpages where dmoz_externalpages.catid in (select dmoz_categories.catid from dmoz_categories where dmoz_categories.mainCategory = '%s')" %(m)
    #print sqlCont
    print m, ShevaDB().dbQuery(sqlCont)
    