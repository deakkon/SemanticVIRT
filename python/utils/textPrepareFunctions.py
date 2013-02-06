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

Functions: 
1. removePunct(text,returnType=2); remove punctuation, default return type string (sentence)
2. removeStopWords(text,mode=2)
3. tokenizersDifference(text,mode=0)
4. testReductionExample(sqlQuery)

"""

#import libraries
import sys, re, nltk, os, string, glob
#from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer, LancasterStemmer
from nltk.corpus import names
from decimal import Decimal
from nltk.corpus import stopwords
from databaseODP import dbQuery
from python.utils import *


#dummy testing data
#not used anymore
#sentence = "Split string by the occurrences of pattern. If capturing parentheses are used in pattern, then the text of all groups in the pattern are also returned as part of the resulting list. If maxsplit is nonzero, at most maxsplit splits occur, and the remainder of the string is returned as the final element of the list. (Incompatibility note: in the original Python 1.5 release, maxsplit was ignored. This has been fixed in later releases.)"
#sql = "select dmoz_newsgroups.catid, dmoz_categories.Description as catDesc from dmoz_categories, dmoz_newsgroups where dmoz_categories.catid = dmoz_newsgroups.catid and dmoz_categories.Description != '' group by dmoz_newsgroups.catid limit 100"


#stemmers
wnl = WordNetLemmatizer()
lst = LancasterStemmer()
ps = PorterStemmer()

#stemming lists
desc = []
desc_seg = []
stopWordsPercentage = []
stemmingPercentage = []

#functions
def removePunct(text,returnType=1):
    """
    Input arguments: text (text to remove punctuation from), returnType (what to return; default string)
    Return types: type list (of words) if returnType = 1, string if returnType = 2 (default)
    
    Removes:
    single letters 
    numbers 
    first male/female names
    punctuation
    """
    #data preparation
    #print "Remove punct ",type(text),"    ",text
    
    if type(text) is str:
        sentence = re.compile('\w+').findall(text)
    elif type(text) is list:
        sentence = text
    else:
        sys.exit("Error with data types. removePunct. textPrepareFunctions")
        
    #print type(sentence),"    ", sentence
    #letter of the alphabet
    allTheLetters = [x for x in string.lowercase]

    if returnType == 1:   
        sentence = [x.lower() for x in sentence]   
        #sentence = removeNames(sentence)
        sentence = [item for item in sentence if item not in allTheLetters]
        sentence = [item for item in sentence if not item.isdigit()]             
    else:
        sentence = ' '.join(sentence)   
    return sentence

def removeNames(text):
    """
    Identifies names
    Input: text, str or list
    Output: removed first male/female names from text, type list
    """    
    #str to list, if needed
    if type(text) is str:
        text = text.split()        
        text = [x.lower() for x in text] 
            
    #list of names
    male_names = names.words('male.txt')
    male_names = [name.lower() for name in male_names]    
    female_names = names.words('female.txt')
    female_names = [name.lower() for name in female_names]
    
    #print list of names
    #print male_names
    #print female_names
    #print text
    noNames = [item for item in text if (item not in male_names and item not in female_names)]
    return noNames  

def removeStopWords(text,mode=1):        
    """
    Removes stop words from text, passed as variable text
    text: type list
    mode -> type of stop words list to use:
        1 = stem words from nltk.corpus.stopwords.words
        2 = stop words from file stopWords.txt (default)
        
    Output: stemmed (Porter stemmer) list of words that are not defined as stopwords, type list
    """
    #print "Remove stop words ",text,"    ",type(text)
    
    #str to list
    """
    if type(text) is str:
        text = text.split()        
        text = [x.lower() for x in text]        
    """
    #variables
    content = []
    
    #choice of stopwords
    if mode == 1:
        stopwords = nltk.corpus.stopwords.words('english')
    elif mode == 2:
        stopwordsFileOpen = open('stopWords.txt','r')
        stopwordsFile = [i.strip() for i in stopwordsFileOpen.readlines()]
    else:
        sys.exit("False flag -> second parameter must be \n 1, if you want to use nltk based set of stopwrods \n 2, if you want to use file based set of stopwords \n")        

    content = removePunct(text)
    content = [w for w in content if w.lower() not in stopwords]
    content = removeNames(content)
    content = [ps.stem(i) for i in content]
    return content

def tokenizersDifference(text,mode=0):
    """
    Dummy function to test difference between tokenizers
    parameters:
    text = text to tokenize
    mode: 
        0 = print results of word_tokenize, wordpunct_tokenize and sent_tokenize on text
        1 = print results of word_tokenize
        2 = print results of wordpunct_tokenize
        3 = print results of sent_tokenize
    """
    if len(text) != 0:
        text = removePunct(text)
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


def testReductionExample(sqlQuery):
    """
    Dummy function, showing reduction effects of removePunct, removeStopWords
    Input: SQL query, specify data to be processed as the first parameter of the query
    """
    #SQL results
    content = dbQuery(sqlQuery)
    
    #go through returned records 
    for record in content:
        desc_WNL = []
        desc_LS = []
        desc_PS = []
        stpWrdPctg = []
        print record[0]
        cleanHtml = nltk.clean_html(record[0])
        print "###########################"
        print "Original sentence ", record[0]
        #tokenizersDifference(cleanHtml,0)
        tokens = nltk.word_tokenize(cleanHtml)
        #tokens = removePunct(cleanHtml, returnType=1)
        #print "Number of tokens: ",len(tokens),"    ",tokens
        #contentNoStopWords = removeStopWords(tokens,2)
        contentNoStopWords = removeStopWords(cleanHtml)
        ratio = Decimal(float(len(contentNoStopWords))/float(len(tokens)))
        stopWordsPercentage.append(ratio)
        stpWrdPctg.append(ratio)
        print "% of stop words in original sentence    ", ratio
        print "Number of tokens w/o SW: ",len(contentNoStopWords),"    ",contentNoStopWords
        #print tokens, "\n"
        for i in contentNoStopWords:
            #WordNet Lemmatizer
            #print "WordNet Lemmatizer", wnl.lemmatize(i)
            desc_WNL.append(wnl.lemmatize(i))
            #Lancaster stemmer
            #print "Lancaster stemmer",lst.stem(i)
            desc_LS.append(lst.stem(i))
            #Porter stemmer
            #print "Porter stemmer", ps.stem(i)
            desc_PS.append(ps.stem(i))
        #print "Recognized names", extract_entity_names(tokens)
        print "WordNet Lemmatization","    ",len(desc_WNL),"    ",desc_WNL
        print "lancaster stemmer","    ",len(desc_LS) ,"    ",desc_LS
        print "Porter stemmer","    ",len(desc_PS) ,"    ",desc_PS
        print "Sentence reduction: ", float(sum(stpWrdPctg)/len(stpWrdPctg))
    print "Overall reduction: ", float(sum(stopWordsPercentage)/len(stopWordsPercentage))
    

def main():
    """
    Functions:
        1. removePunct(text,returnType=2); remove punctuation, default return type string (sentence)
        2. removeStopWords(text,mode=2)
        3. tokenizersDifference(text,mode=0)
        4. removeNames(text)
        5. testReductionExample(sqlQuery)
        
           anything else for exit    
    """ 
    print main.__doc__
    
    var = raw_input("Choose a function: ")
        
    if var == "1":        
        print removePunct.__doc__
        var1 = raw_input("Enter text to remove punctuation: ")
        print removePunct(var1)
    elif var == "2":
        print removeStopWords.__doc__
        var1 = raw_input("Enter text to remove stop words: ")
        print removeStopWords(var1)
    elif var == "3":
        print tokenizersDifference.__doc__
        var1 = raw_input("Enter text to remove stop words: ")
        print tokenizersDifference(var1)   
    elif var == "4":
        print removeNames.__doc__
        var1 = raw_input("Text to remove names from: ")        
        print removeNames(var1)  
    elif var == "5":
        print testReductionExample.__doc__
        var1 = raw_input("Text to remove names from: ")        
        print testReductionExample(var1)               
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
        

if __name__ == '__main__':    
    main()