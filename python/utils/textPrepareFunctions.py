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
import sys, re, nltk
#from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer, LancasterStemmer
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
def removePunct(text,returnType=2):
    """
    Input arguments: text (text to remove punct from), returnType (what to return; default string)
    Return types: type list of words if returnType = 1, string if returnType = 2 (default)
    """
    sentence = re.compile('\w+').findall(text)
    #sentence = re.sub("[^a-zA-Z]", "", text)
    #sentence = " ".join([x for x in text.split(" ") if not x.isdigit()])
    #print "rp sentence: ",sentence
    if returnType == 1:   
        sentence = [x.lower() for x in sentence]              
        return sentence
    else:
        sentenceReturn = ' '.join(sentence)
        return sentenceReturn      

def removeStopWords(text,mode=2):        
    """
    Removes stop words from text, passed as variable text 
    Node -> type of stemmer to use
        1 = stem words from nltk.corpus.stopwords.words
        2 = stop words from file stopWords.txt (default)
        
    Output: type list of words that are not defined as stopwords
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
        contentNoStopWords = removeStopWords(removePunct(cleanHtml, returnType=1),2)
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
        4. testReductionExample(sqlQuery)
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
        print testReductionExample.__doc__
        var1 = raw_input("Insert SQL query: ")        
        print testReductionExample(var1)      
    else:
        print "Hm, ", var," not supported as an options"
        sys.exit(1)
        

if __name__ == '__main__':    
    main()