import nltk, string
from nltk.corpus import brown,gutenberg,reuters

"""
for genre in brown.categories():
    categories.append(genre)
    print genre
    
for word in brown.words():
    words.append(word)
    print word 



"""
cfd = nltk.ConditionalFreqDist(
          (genre, word)
          for genre in brown.categories()
          for word in brown.words(categories=genre))
genres = ['news', 'religion', 'hobbies', 'science_fiction', 'romance', 'humor']
modals = ['can', 'could', 'may', 'might', 'must', 'will']
cfd.tabulate(conditions=genres, samples=modals)