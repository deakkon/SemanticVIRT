import sys
sys.path.append("/home/jseva/SemanticVIRT/_utils/")
from ShevaTPF import ShevaTPF as stpf

text = "<p>When history has a different script from the one in your films, who wouldn't invent a country to fool themselves? The collapsing sets of Tito's Hollywood of the East take us on a journey through the rise and fall of the illusion called Yugoslavia. Exploring the ruins of the forgotten film sets and talking to directors, producers, policemen and Tito's projectionist about the state run film studios and Tito's personal love for cinema and it's stars, 'Cinema Komunisto' uses film clips to go back to the film when 'His story' became the official history.<em class='nobr'>Written by <a href='/search/title?plot_author=Anonymous&amp;view=simple&amp;sort=alpha&amp;ref_=tt_stry_pl'>Anonymous</a></em></p>"
#print text
tpf = stpf()
#print tpf.removeHtmlTags(text.split())
#print tpf.stripHTMLTags(text)
#print tpf.removeStopWords(text.split(),1)
#print tpf.removeStopWords(text.split(),2)
print tpf.returnClean(text,1), len(tpf.returnClean(text,1))
print tpf.returnClean(text,2), len(tpf.returnClean(text,2))