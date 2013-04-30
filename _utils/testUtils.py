import os
from ShevaUtils import *

"""
print("Path at terminal when executing this file")
print(os.getcwd() + "\n")

print("This file path, relative to os.getcwd()")
print(__file__ + "\n")

print("This file full path (following symlinks)")
full_path = os.path.realpath(__file__)
print(full_path + "\n")

print("This file directory and name")
path, file = os.path.split(full_path)
print(path + ' --> ' + file + "\n")

print("This file directory only")
print(os.path.dirname(full_path))
"""
lista = ["1","2","3"]
listaT = ("1","2","3")
nekiString ="aaaaaaaaaaaaa"

"""
print ShevaUtils().checkIfList(nekiStgring)
print ShevaUtils().checkIfList(lista)
print ShevaUtils().checkIfList(listaT)
"""
print ShevaUtils().write2CSV(nekiString,1,1)
