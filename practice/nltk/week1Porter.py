import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import WhitespaceTokenizer 

tekst = "In linguistic morphology and information retrieval, stemming is the process for reducing inflected words to their stem, base or root form-generally a written word form. The stem need not be identical to the morphological root of the word; it is usually sufficient that related words map to the same stem, even if this stem is not in itself a valid root. Algorithms for stemming have been studied in computer science since 1968. Many search engines treat words with the same stem as synonyms as a kind of query broadening, a process called conflation."
tokens = nltk.word_tokenize(tekst)

#porter stemmer
porter = nltk.PorterStemmer()
lancaster = nltk.LancasterStemmer()

for t in tokens:
    stemiran = porter.stem(t)
    #print stemiran

[porter.stem(t) for t in tokens]


#tokenizer
#print 'tokenizer'
text = "The AU was originally defined as the length of the semi-major axis of the Earth's elliptical orbit around the Sun. In 1976 the International Astronomical Union revised the definition of the AU for greater precision, defining it as that length for which the Gaussian gravitational constant (k) takes the value 0.017 202 098 95 when the units of measurement are the astronomical units of length, mass and time.[5][6][7] An equivalent definition is the radius of an unperturbed circular Newtonian orbit about the Sun of a particle having infinitesimal mass, moving with an angular frequency of 0.017 202 098 95 radians per day,[2] or that length for which the heliocentric gravitational constant (the product GM) is equal to (0.017 202 098 95)2 AU3/d2. It is approximately equal to the mean Earth-Sun distance."

#non alphanumeric regexp
print "non alphanumeric regexp"
tokenizer1 = RegexpTokenizer('[^A-Za-z0-9]',gaps='false')
ispis1 = tokenizer1.tokenize(text)
print ispis1
print len(ispis1)

#whitespace 
print "whitespace"
tokenizer2 = WhitespaceTokenizer() 
rez2 = tokenizer2.tokenize(text)
print rez2
print len(rez2)

#Levenshtein distance
string1 = "bane"
string2 = "barn"
levdist = nltk.edit_distance(string1, string2)
print "levdist: %s" % levdist 
