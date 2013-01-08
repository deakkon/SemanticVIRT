from sys import argv

script, filename = argv

print "Erasing %r" %filename
print "To cancel print CTRL-C"
print "Too confirm, press enter"

raw_input("?")

print "Opening file..."
target = open(filename,'w')

print "Truncating file. Goodbye!"
target.truncate()

print "Now im going to ask you for the three lines"

line1 = raw_input("line 1:")
line2 = raw_input("line 2:")
line3 = raw_input("line 3:")
tekst = line1+"\n"+line2+"\n"+line3+"\n"
print tekst
target.write(tekst)

print "Writing lines to file"

"""
target.write(line1)
target.write("\n")
target.write(line2)
target.write("\n")
target.write(line3)
target.write("\n")
"""
print "Finally, closing"
target.close()