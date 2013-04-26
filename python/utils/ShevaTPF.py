#!/usr/bin/python
# -*- coding: utf8 -*-
"""
Text preparation functions for further vectorization etc.
"""

#import libraries
import sys, re, nltk, os, string, glob
from nltk.stem import WordNetLemmatizer, PorterStemmer, LancasterStemmer
from nltk.corpus import names
from nltk.corpus import stopwords
from urlparse import urlparse
from postmarkup import render_bbcode
from lxml import html

class ShevaTPF:

    def __init__(self, text, type):
        self.text = text
        self.type = type

    def string2list(self, text):
        sentence = []
        if type(text) is str:
            sentence = re.compile('\w+').findall(text)
        elif type(text) is list:
            sentence = text
        else:
            sys.exit("Error with data types. removePunct. textPrepareFunctions")
        return sentence
        
    def removeNames(self, text):
        sentence = []
        #name files
        male_names = nltk.corpus.names.words('male.txt')
        male_names = [name.lower() for name in male_names]
        female_names = nltk.corpus.names.words('female.txt')
        female_names = [name.lower() for name in female_names]
        #remove names
        sentence = [item.lower() for item in text if (item not in male_names and item not in female_names)]
        #return names
        return sentence

    def removeAN(self, text):
        sentence = []
        allTheLetters = [x for x in string.lowercase]
        sentence = [x.lower() for x in text]
        sentence = [item for item in sentence if item not in allTheLetters]
        sentence = [item for item in sentence if not item.isdigit()]
        return sentence

    def removeHtmlTags(self, text):
        text = " ".join(text)
        doc = html.document_fromstring(text)
        bbcode = doc.text_content()
        content = render_bbcode(bbcode)
        return content
    
    def removeStopWords(self, text, mode=1):
        """
        Removes stop words from text, passed as variable text
        text: type list
        mode -> type of stop words list to use:
            1 = stem words from nltk.corpus.stopwords.words
            2 = stop words from file stopWords.txt (default)
        Output: stemmed (Porter stemmer) list of words that are not defined as stopwords, type list
        """
        sentence = []

        if mode == 1:
            stopwords = nltk.corpus.stopwords.words('english')
        elif mode == 2:
            stopwordsFileOpen = open('stopWords.txt','r')
            stopwordsFile = [i.strip() for i in stopwordsFileOpen.readlines()]
        else:
            sys.exit("False flag -> second parameter must be \n 1, if you want to use nltk based set of stopwrods \n 2, if you want to use file based set of stopwords \n")        
    
        sentence = [w for w in text if w.lower() not in stopwords]
        return sentence
    
    def returnStem(self, text, type=1):
        sentence = []
        if type == 1:
            stemmer = PorterStemmer()
        elif type == 2:
            stemmer = LancasterStemmer()
        elif type == 3:
            stemmer = WordNetLemmatizer()
        else:
            sys.exit("Something wrong with stemmer")
            
        sentence = [stemmer.stem(wordItem) for wordItem in text]
        return sentence
    
    def returnClean(self):
        sentence = []
        sentence = self.string2list(self.text)
        #sentence = self.removeHtmlTags(sentence)
        sentence = self.removeNames(sentence)
        sentence = self.removeAN(sentence)
        sentence = self.removeStopWords(sentence,self.type)
        sentence = self.returnStem(sentence)
        return sentence