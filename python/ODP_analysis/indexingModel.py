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
import sys, os
#db
import MySQLdb
#nltk
import nltk
#tokenization
from nltk import tokenize, stem
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
#stemmers
from nltk.stem import WordNetLemmatizer, PorterStemmer, LancasterStemmer

#stop words
from nltk.corpus import stopwords

#stemmers
wnl = WordNetLemmatizer()
lst = LancasterStemmer()
ps = PorterStemmer()

#stemming lists
desc = []
desc_seg = []
#empty name list


def dbConnect(sql):
    """
    Basic dB functionality
    """
    db = MySQLdb.connect(host="localhost", user="root", passwd="", db="dmoz_new")
    c = db.cursor()
    rez = c.execute(sql)
    return c.fetchall()

def tokenizersDifference(text,mode):
    """
    parameters:
    text = text to tokenize
    mode: 
        0 = print results of word_tokenize, wordpunct_tokenize and sent_tokenize on text
        1 = print results of word_tokenize
        2 = print results of wordpunct_tokenize
        3 = print results of sent_tokenize
    """
    if len(text) != 0:
        if mode == 0:
            print "word_tokenize", "    ",nltk.word_tokenize(text)
            print "wordpunct_tokenize", "    ",nltk.wordpunct_tokenize(text)
            print "sent_tokenize", "    ",nltk.sent_tokenize(text)
        elif mode == 1:
            print nltk.word_tokenize(text)
        elif mode == 2:
            print nltk.wordpunct_tokenize(text)
        elif mode == 3:
            print nltk.sent_tokenize(text)
        else:
            sys.exit("False flag -> second parameter must be \n0 = print results of word_tokenize, wordpunct_tokenize and sent_tokenize on text\n1 = print results of word_tokenize\n2 = print results of wordpunct_tokenize\n3 = print results of sent_tokenize")
    else:
        sys.exit("text string to tokenize is empty")
        
def removeStopWords(text,mode):        
    """
    remove stop words; 1 = stem words from nltk.corpus.stopwords.words
    2 = stop words from file stopWords.txt
    """
    content = []
    
    if mode == 1:
        stopwords = nltk.corpus.stopwords.words('english')
        content = [w for w in text if w.lower() not in stopwords]
        #print len(content)/len(text)
        return content
    elif mode == 2:
        stopwordsFileOpen = open('stopWords.txt','r')
        stopwordsFile = [i.strip() for i in stopwordsFileOpen.readlines()]
        content = [w for w in text if w.lower() not in stopwordsFile]
        stopwordsFileOpen.close()
        #print len(content)/len(text)
        return content
    else:
        sys.exit("False flag -> second parameter must be \n 1, if you want to use nltk based set of stopwrods \n 2, if you want to use file based set of stopwords \n")

def extract_entity_names(t):
    entity_names = []
    
    if hasattr(t, 'node') and t.node:
        if t.node == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))
                
    return entity_names
sql = "select dmoz_newsgroups.catid, dmoz_categories.Description as catDesc from dmoz_categories, dmoz_newsgroups where dmoz_categories.catid = dmoz_newsgroups.catid and dmoz_categories.Description != '' group by dmoz_newsgroups.catid limit 100"
rowCount = dbConnect(sql)

for record in rowCount:
    """
    simple tokenization & stemming
    taking results of an SQL query
    name recognition
    """
    desc_WNL = []
    desc_LS = []
    desc_PS = []
    names = []
    cleanHtml = nltk.clean_html(record[1])
    print "###########################"
    #tokenizersDifference(cleanHtml,0)
    tokens = nltk.word_tokenize(cleanHtml)
    print "number of tokens: ",len(tokens),"    ",tokens
    contentNoStopWords = removeStopWords(tokens,1)
    print "number of tokens w/o SW: ",len(contentNoStopWords),"    ",contentNoStopWords
    #print tokens, "\n"
    for i in contentNoStopWords:
        #WordNet Lemmatizer
        #print wnl.lemmatize(i)
        desc_WNL.append(wnl.lemmatize(i))
        #Lancaster stemmer
        #print lst.stem(i)
        desc_LS.append(lst.stem(i))
        #Porter stemmer
        #print ps.stem(i)
        desc_PS.append(ps.stem(i))
    
    for tree in chunked_sentences:
        # Print results per sentence
        # print extract_entity_names(tree)    
        entity_names.extend(extract_entity_names(tree))        
    print "Recognized names", extract_entity_names(tokens)
    print len(desc_WNL) ,"WordNet Lemmatization","    ",desc_WNL
    print len(desc_LS) ,"lancaster stemmer","    ",desc_LS
    print len(desc_LS) ,"Porter stemmer","    ",desc_PS