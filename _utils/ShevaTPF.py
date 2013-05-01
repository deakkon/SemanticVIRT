#import libraries
import sys, re, nltk, os, string, glob, urlparse, types
from nltk.stem import WordNetLemmatizer, PorterStemmer, LancasterStemmer
from nltk.corpus import names
from nltk.corpus import stopwords
from nltk.tokenize.punkt import PunktWordTokenizer
from urlparse import urlparse
from postmarkup import render_bbcode
from lxml import html
from bs4 import BeautifulSoup
from bs4 import BeautifulStoneSoup

class ShevaTPF:
    """
    def __init__(self):
        print "Calling parent constructor"
        self.text = text
        self.typeModus = typeModus
    """

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
        
        if isinstance(text, types.ListType): 
            text = " ".join(text)

        sentence = ' '.join(BeautifulSoup(text).findAll(text=True))
        sentence = sentence.encode('utf8')
        sentence = sentence.split()
        return sentence
    
    def stripHTMLTags(self, text):
        if isinstance(text, types.ListType):
            text = " ".join(str(text))

        # apply rules in given order!
        rules = [
        { r'>\s+' : u'>'},                  # remove spaces after a tag opens or closes
        { r'\s+' : u' '},                   # replace consecutive spaces
        { r'\s*<br\s*/?>\s*' : u'\n'},      # newline after a <br>
        { r'</(div)\s*>\s*' : u'\n'},       # newline after </p> and </div> and <h1/>...
        { r'</(p|h\d)\s*>\s*' : u'\n\n'},   # newline after </p> and </div> and <h1/>...
        { r'<head>.*<\s*(/head|body)[^>]*>' : u'' },     # remove <head> to </head>
        { r'<a\s+href="([^"]+)"[^>]*>.*</a>' : r'\1' },  # show links instead of texts
        { r'[ \t]*<[^<]*?/?>' : u'' },            # remove remaining tags
        { r'^\s+' : u'' }                   # remove spaces at the beginning
        ]
        
        for rule in rules:
            for (k,v) in rule.items():
                regex = re.compile (k)
                text  = regex.sub (v, text)
        
        # replace special strings
        special = {'&nbsp;' : ' ', '&amp;' : '&', '&quot;' : '"','&lt;'   : '<', '&gt;'  : '>'
        }
        
        for (k,v) in special.items():
            text = text.replace (k, v)
        
        text = str(text)
        return text.split()

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
            stopwordsFile = open('stopWords.txt','r')
            stopwords = [i.strip() for i in stopwordsFile.readlines()]
            #print stopwords
        else:
            sys.exit("False flag -> second parameter must be \n 1, if you want to use nltk based set of stopwrods \n 2, if you want to use file based set of stopwords \n")        
    
        sentence = [w for w in text if w.lower() not in stopwords]
        return sentence
    
    def returnStem(self, text, typeModus=1):
        sentence = []
        if typeModus == 1:
            stemmer = PorterStemmer()
        elif typeModus == 2:
            stemmer = LancasterStemmer()
        elif typeModus == 3:
            stemmer = WordNetLemmatizer()
        else:
            sys.exit("Something wrong with stemmer")

        sentence = [stemmer.stem(wordItem) for wordItem in text]
        return sentence
    
    def returnClean(self,sentence,typeModus):

        sentence = self.string2list(sentence)
        #print sentence
        sentence = self.stripHTMLTags(sentence)
        #print sentence
        sentence = self.removeHtmlTags(sentence)
        #print sentence
        sentence = self.removeNames(sentence)
        #print sentence
        sentence = self.removeAN(sentence)
        #print sentence
        sentence = self.removeStopWords(sentence,typeModus)
        #print sentence
        sentence = self.returnStem(sentence)
        return sentence