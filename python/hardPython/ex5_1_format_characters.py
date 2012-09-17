name= "Jurica Seva"
age= 30
height = 187 #cm 
weight = 78 #kg
eyes= "brown"
teeth = "White"
hair = "brown/bald"

print "Let's talk about %s" %name
print "He's %d inches tall." %height
print "he's %d pounds heavy."
print "Actually that's not too heavy."
print "He's got %s eyes and %s hair." %(eyes,hair)
print "His teeth are usually %s depending on the coffee." %teeth

#this line is tricy
print "if i add %x, %x, and %x I get %x" % (age,height, weight, age+ height + weight)

"""
fromat characters
d    Signed integer decimal.    
i    Signed integer decimal.    
o    Unsigned octal.    (1)
u    Unsigned decimal.    
x    Unsigned hexadecimal (lowercase).    (2)
X    Unsigned hexadecimal (uppercase).    (2)
e    Floating point exponential format (lowercase).    (3)
E    Floating point exponential format (uppercase).    (3)
f    Floating point decimal format.    (3)
F    Floating point decimal format.    (3)
g    Floating point format. Uses exponential format if exponent is greater than -4 or less than precision, decimal format otherwise.    (4)
G    Floating point format. Uses exponential format if exponent is greater than -4 or less than precision, decimal format otherwise.    (4)
c    Single character (accepts integer or single character string).    
r    String (converts any python object using repr()).    (5)
s    String (converts any python object using str()).    (6)
%    No argument is converted, results in a "%" character in the result.    

"""