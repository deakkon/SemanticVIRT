#stop words from file
def content_fraction():
    text = "In WordNet, words are organized whatever according to their meanings or senses. A set of words that can be synonyms (having the same meaning) are grouped into a synonym set, called a \"synset\" in WordNet. As we have already done part-of-speech tagging, we can use the POS tags to improve the way we access WordNet. When we access a word's synset (synonym set), we can restrict this to the specific part of speech."
    text = text.split()
    
    stopwordsFileOpen = open('stopWords.txt','r')
    stopwordsFile = [i.strip() for i in stopwordsFileOpen.readlines()]
    print stopwordsFile
    content = [w for w in text if w.lower() not in stopwordsFile]
    print content
    return float(len(content)/len(text))
    stopwordsFileOpen.close()
    
print content_fraction()