from sys import path
path.append("/home/jseva/SemanticVIRT/python/utils/")

from ShevaTPF import ShevaTPF

text = "i was ALWAYS dreaming about the sunsets over the hill in the blah. maria.<html><h1>"
tfp = ShevaTPF(text,1)
tfpResult = tfp.returnClean()

print text,"\n"
print tfpResult 