from nltk.corpus import reuters, inaugural, wordnet
"""
nazivi = reuters.fileids()
print nazivi
kat = reuters.categories()
print kat
print reuters.categories('training/9865')
print reuters.fileids(['barley', 'corn'])
"""
print inaugural.fileids()
print [fileid[:4] for fileid in inaugural.fileids()]