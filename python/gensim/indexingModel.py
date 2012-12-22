#!/usr/bin/python
# -*- coding: utf8 -*-
"""
Pseudocode taken from: IMPLEMENTING A VECTOR SPACE DOCUMENT RETRIEVAL SYSTEM, Mark A. Greenwood, http://www.dcs.shef.ac.uk/~mark/nlp/pubs/vspace.pdf
PSEUDOCODE:
1. Read in a line at a time from the db/file containing the document collection, until an entire document has been read in.
2. Split the document into tokens; remove any stop words present (if the user has requested) and stem the resulting tokens (if the user has requested).
For each token in the document/db storage (line in db matching SQL query):
    Get a reference to the hash of documents - word counts for this word
    If the hash exists then this word has been seen before so
        Get the word count for the current document, for this word
        If this exists
            add one to it and put it back in the hash
        else
            set the count to 1 and store it against this document in the document word count hash
    else
        store a reference to an anonymous hash containing this document and a count of 1 against this word in the index
Store the length of the document in terms as we will need this as well
Repeat until there are no more documents (descriptions from database in our case)

Created on 18.10.2012.

@author: Jurica Seva, PhD candidate
"""

""" import libraries """
#db
import MySQLdb
#nltk
import nltk
#tokenization
from nltk import tokenize, stem
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
#stemmers
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
#stop words
from nltk.corpus import stopwords

"""
get stuff from db
"""
db = MySQLdb.connect(host="localhost", user="root", passwd="", db="dmoz_new")
c = db.cursor()
rez = c.execute("select dmoz_newsgroups.catid, dmoz_categories.Description as catDesc from dmoz_categories, dmoz_newsgroups where dmoz_categories.catid = dmoz_newsgroups.catid and dmoz_categories.Description != '' group by dmoz_newsgroups.catid limit 100")
rowCount = c.fetchall()

#stemmers
wnl = WordNetLemmatizer()
lst = LancasterStemmer()
ps = PorterStemmer()

#stemming lists
desc = []
desc_seg = []
desc_WNL = []
desc_LS = []
desc_PS = []

def content_fraction(text,mode):        
    """
    stop words, percentage of stop words in text
    """
    #built in stopwords
    if mode == 1:
        stopwords = nltk.corpus.stopwords.words('english')
        content = [w for w in text if w.lower() not in stopwords]
        return len(content) / len(text)
    elif mode == 2:
        #stop words from file
        stopwordsFile = open('stopWords.txt','r')
        content = [w for w in text if w.lower() not in stopwords]
        return len(content) / len(text)
    else:
        print "False flag -> second parameter must be \n"
        print "1 if you want to use nltk based set of stopwrods \n"
        print "2 if you want to use file based set of stopwords \n"
        return False

#simple tokenization & stemming
for record in rowCount:
    desc_WNL = []
    desc_LS = []
    desc_PS = [] 
    #print record[0],"  ->  ",record[1]
    #if record[1] != "":
    desc.append(record[1])
    cleanHtml = nltk.clean_html(record[1])
    print cleanHtml, "\n"
    #percentage of stop words in text, line by line    
    print "% of stop words in sentence above: " 
    print content_fraction(record[1])
    #tokens
    tokens = nltk.word_tokenize(cleanHtml)   
    #print tokens, "\n"
    for i in tokens:
        #WordNet Lemmatizer
        #print wnl.lemmatize(i)
        desc_WNL.append(wnl.lemmatize(i))
        #Lancaster stemmer
        #print lst.stem(i)
        desc_LS.append(lst.stem(i))
        #Porter stemmer
        #print ps.stem(i)
        desc_PS.append(ps.stem(i))
    print "###########################"
    print "WordNet Lemmatization"
    print desc_WNL
    print len(desc_WNL) 
    print "###########################"
    print "lancaster stemmer"
    print desc_LS
    print len(desc_LS)
    print "###########################"
    print "Porter stemmer"
    print desc_PS
    print len(desc_PS)
    print "###########################"
    
    #desc_seg.append(object)
"""
#individual words ->         
for i in desc:
    #print i,"\n"
    words = i.split(" ")    
    k=0
    j = len(words)    
    while k < j:
        print words[k]
        k += 1
#print desc
#print len(desc)
"""