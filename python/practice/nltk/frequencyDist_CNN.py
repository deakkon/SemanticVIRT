'''
Created on 30.1.2012.

@author: Jurica 
'''

import nltk

from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import CategorizedPlaintextCorpusReader
 
genesis_dir = nltk.data.find('corpora\\cnn')
print genesis_dir
print nltk.corpus.genesis.root 