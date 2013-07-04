#import libraries
import sys, re, nltk, os, string, glob, urlparse, types, collections
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
    
    
    def __init__(self):
        """
        Works with nested lists (list of lists: [['str1','str2','str3',...,'strn'],[],[],[]]
        """
        self.table = string.maketrans("","")
        self.male_names =  [name.lower() for name in nltk.corpus.names.words('male.txt')] 
        self.female_names = [name.lower() for name in nltk.corpus.names.words('female.txt')] 
        self.stopwords = nltk.corpus.stopwords.words('english')
        print "ShevaTPF created"
        
    def __del__(self):
        print 'ShevaTPF destroyed'        

    def checkList(self,text):
        if isinstance(x, types.ListType):
            pass
        else:
            sys.exit("Passed argument is not string. ShevaTPF.checkList.")

    def getUniqueTokens(self, text):
        sentence = []
        merged = list(itertools.chain.from_iterable(text))
        #print merged
        count = collections.Counter(merged)
        sentence.extend([elt.lower() for elt,count in count.most_common() if count == 1])
        return sentence
    
    def removeUniqueTokens(self,text, nestedList):
        #sentence = []
        sentence = [item for item in text if item not in self.getUniqueTokens(nestedList)]
        return sentence
    
    def removePunctuation(self,text):
        #sentence = []
        sentence = [s.translate(self.table, string.punctuation) for s in text]
        return sentence
    
    def removeSpecialHTML(self,text):
        sentence = []

        # replace special strings
        special = {'&nbsp;' : ' ', '&amp;' : '&', '&quot;' : '"','&lt;'   : '<', '&gt;'  : '>'}
        
        for item in text:
            for (k,v) in special.items():
                item = item.replace (k, v)
            sentence.append(item.lower())
            #print item
        
        return sentence 

    def removeNames(self, text):
        sentence = [item for item in text if (item not in self.male_names and item not in self.female_names)]
        return sentence

    def removeAN(self, text):
        sentence = []
        allTheLetters = [x for x in string.lowercase]
        #sentence = [x for x in text]
        sentence = [item for item in text if item not in allTheLetters]
        sentence = [item for item in text if not item.isdigit()]
        return sentence

    def removeHtmlTags(self, text):
        if isinstance(text, types.ListType): 
            text = " ".join(text)

        sentence = ' '.join(BeautifulSoup(text).findAll(text=True))
        sentence = sentence.encode('utf8')
        sentence = sentence.split()
        return sentence

    def removeStopWords(self, text, mode=1):
        """
        Removes stop words from text, passed as variable text
        text: type list
        mode -> type of stop words list to use:
            1 = stem words from nltk.corpus.stopwords.words
            2 = stop words from file stopWords.txt (default)
        Output: stemmed (Porter stemmer) list of words that are not defined as stopwords, type list
        """
        #sentence = []

        if mode == 1:
            stopwords = self.stopwords
        elif mode == 2:
            stopwordsFile = open('stopWords.txt','r')
            stopwords = [i.strip() for i in stopwordsFile.readlines()]
            #print stopwords
        else:
            sys.exit("False flag -> second parameter must be \n 1, if you want to use nltk based set of stopwrods \n 2, if you want to use file based set of stopwords \n")        
    
        sentence = [w for w in text if w not in stopwords]
        return sentence
    
    def returnStem(self, text, typeModus=1):
        #sentence = []
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
    
    def returnClean(self,text,typeModus):
        
        contentLenght = range(0,len(text))
        
        for i in contentLenght:
            sentence = text[i]
            sentence = self.removeSpecialHTML(sentence)
            #print sentence
            sentence = self.removePunctuation(sentence)
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
            text[i] = sentence
        return text