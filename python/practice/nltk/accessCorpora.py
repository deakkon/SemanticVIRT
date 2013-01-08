import nltk
import string
from nltk.corpus import gutenberg, webtext, brown
gutenberg.fileids()
emma = gutenberg.words('austen-emma.txt')
""" this is a multiline comment
print emma
for fileid in gutenberg.fileids():
    num_chars = len (gutenberg.raw(fileid))
    num_words = len (gutenberg.raw(fileid))
    num_sents = len (gutenberg.sents(fileid))
    num_vocab = len(set([w.lower() for w in gutenberg.words(fileid)]))
    print fileid, int(num_chars/num_words),int(num_words/num_sents), int(num_words/num_vocab)
    
    
    
macbeth_sentences = gutenberg.sents('shakespeare-macbeth.txt')
macbeth_sentences

for fields in webtext.fileids():
    print fields, webtext.raw(fields )[:65], '...'

#kategorija korpusa
print('\n')
kat = brown.categories()
for kat in kat:
    print kat
 
#analiza hobi -> kolko rijeci iz modals ima u toj kategoriji
hobi = brown.words(categories='hobbies')
fdist = nltk.FreqDist([w.lower() for w in hobi])
modals = ['can', 'could', 'may', 'might', 'must', 'will']
for m in modals:
    print m + ':', fdist[m],
""" 
#sf
sf = brown.words(categories='science_fiction')
fdist = nltk.FreqDist([w.lower() for w in sf])
rijeci = []
for i in sf:
    if i.startswith('wh'):
        #print i
        rijeci.append(i)
        
for r in rijeci:
    print r + ':', fdist[r],