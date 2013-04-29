from sys import path
path.append("/home/jseva/SemanticVIRT/python/utils/")
#from ShevaTPF import *
from ShevaTPF import ShevaTPF as stpf

text = "i was ALWAYS dreaming about the sunsets over the hill in the blah. maria.<html><h1> aaaaaaaaaa"

tpf = stpf()
#tpf = ShevaTPF(text,1)


tpfResult = tpf.returnClean(text,1)

print text,"\n"
print tfpResult