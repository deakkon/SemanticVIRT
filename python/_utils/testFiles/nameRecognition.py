'''
Created on 17.12.2012.

@author: Jurica
'''
import nltk
from nltk.corpus import names
names = nltk.corpus.names
print names
male_names = names.words('male.txt')
print male_names

female_names = names.words('female.txt')
print female_names
"""
with open('sample.txt', 'r') as f:
    sample = f.read()
 
sentences = nltk.sent_tokenize(sample)
print sentences

tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
print "TS    ", tokenized_sentences

tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
print "TS    ", tagged_sentences

chunked_sentences = nltk.batch_ne_chunk(tagged_sentences, binary=True)
print "CS    ", chunked_sentences
 
def extract_entity_names(t):
    entity_names = []
    
    if hasattr(t, 'node') and t.node:
        if t.node == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))
                
    return entity_names
 
entity_names = []
for x in chunked_sentences:
    # Print results per sentence
    # print extract_entity_names(tree)    
    entity_names.extend(extract_entity_names(x))
 
# Print all entity names
print entity_names
 
# Print unique entity names
print set(entity_names)
"""