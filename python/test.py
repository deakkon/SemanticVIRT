#stop words from file
def content_fraction():
    text = "In WordNet, words are organized according to their meanings or senses. A set of words that can be synonyms (having the same meaning) are grouped into a synonym set, called a \"synset\" in WordNet. As we have already done part-of-speech tagging, we can use the POS tags to improve the way we access WordNet. When we access a word's synset (synonym set), we can restrict this to the specific part of speech."
    stopwordsFile = open('stopWords.txt','r')
    print len(stopwordsFile)
    print stopwordsFile
    content = [w for w in text if w.lower() not in stopwordsFile]
    return len(content) / len(text)

print content_fraction()