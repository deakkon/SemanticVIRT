import sys
import itertools
import collections
sys.path.append("/home/jseva/SemanticVIRT/_utils/")
from ShevaTPF import ShevaTPF
shevaTPF = ShevaTPF()


content =  [['Portfolio', 'of', 'photography.', 'of', 'examples', 'of', 'work,', 'a', 'travel', 'journal', 'of', 'her', 'journey', 'through', 'Asia', 'and', 'contact', 'information.', 'Photojournalism', 'works', 'about', 'Indonesia', 'by', 'Zarqoni', 'Maksum,', 'professional', 'photojourlist', 'based', 'in', 'Jakarta.', 'Newspaper', 'photographer', 'in', 'Boulder,', 'Colorado,', 'US.', 'She', 'provides', 'professional', 'photography', 'services', 'for', 'editorial,', 'advertising,', 'and', 'corporate', 'projects.', 'Portfolio', 'and', 'contact', 'details', 'of', 'this', 'Israelian', 'photojournalist.', 'Photographer', 'specializing', 'in', 'location', 'photography,', 'photojournalism,', 'editorial', 'photography', 'and', 'corporate', 'photography.', 'Based', 'in', 'Johannesburg,', 'South', 'Africa.', 'Biography', 'and', 'samples', 'of', 'work', 'from', 'the', 'photojournalist', 'based', 'in', 'Malta', 'who', 'has', 'covered', 'topics', 'including', 'London', 'riots,', 'the', 'Bosnian', 'war,', 'Kosovo', 'refugee', 'crisis,', 'and', 'post-communist', 'Albania.'], ['About', 'his', 'life', 'and', 'work.', 'Exhibitions', 'will', 'be', 'organized', 'from', 'the', 'collection,', 'as', 'well', 'as', 'of', 'other', 'artists.', 'Tete', 'a', 'Tete:', 'Portraits', 'by', 'Henri', 'Cartier-Bresson,', 'including', 'Truman', 'Capote', 'and', 'Coco', 'Chanel.', '20th', 'century', 'master', 'of', 'the', 'candid', 'photograph.', 'Called', '&quot;the', 'father', 'of', 'photojournalism.&quot;', 'Gallery', 'M', 'gives', 'a', 'biography', 'and', 'shows', 'several', 'of', 'his', 'photos.','&nbsp;']]

"""
content = [[1,2,3],[4,5,6],[7,8,9],[10,11,12],[13,14,15]]
expandedC = []
a = 0

while a < 5:
    expandedC.extend(content)
    a += 1

print expandedC

#print len(content)
contentLenght = range(0,len(content))

print contentLenght

for i in contentLenght:     
print content[i]
"""
    #print shevaTPF.returnClean(content[i],1) 
#print shevaTPF.returnClean(content,1)
   
"""
# remove common words and tokenize
stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]

# remove words that appear only once
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once]
         for text in texts]

print texts
"""
sentence=[]
merged = list(itertools.chain.from_iterable(content))
#print merged
x=collections.Counter(merged)
#print(x.most_common())
sentence.extend([elt for elt,count in x.most_common() if count == 1])
print sentence