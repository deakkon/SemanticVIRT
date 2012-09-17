from sys import argv

script, filename = argv

print "Opening file %r" %filename

traget = open(filename,'r')
print traget.read()