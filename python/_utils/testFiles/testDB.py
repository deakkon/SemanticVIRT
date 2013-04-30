from sys import path
#from ShevaDB import ShevaDB as baza
from ShevaDB import *

print ShevaDB().dbQuery("select * from analysis_f1")