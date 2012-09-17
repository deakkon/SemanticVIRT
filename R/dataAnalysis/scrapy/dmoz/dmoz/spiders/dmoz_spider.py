from scrapy.item import Item,Field
from scrapy.contrib.spiders import CrawlSpider
from scrapy.spider import BaseSpider
import MySQLdb
  
class MininovaSpider(BaseSpider):
    name = 'ffhist'
    start_urls = ['www.cnn.com']
    #list elements
    urlListDB = []
    urlList = []
    #print urlList
    #database stuff, fill the list with urls    
    db = MySQLdb.connect("localhost", user="root",passwd="", db="test")   
    cursor = db.cursor()
    cursor.execute("select sessionID, URL from datahistory") 
    result = cursor.fetchall()
    for record in result:
        #print record[0] , "-->", record[1]    
        urlListDB.append([record[0],record[1]])
    start_urls = urlListDB
    len = len(start_urls)
    for row in range(0,len):
        urlList.append(start_urls[row][1])
        def parse(self, response):
            hxs = HtmlXPathSelector(response)
            hxs.select("//h1")
            hxs.select("//h1/text").extract()
            sites = hxs.select('//ul/li')
        print start_urls[row][1]
        
    """
    name = 'dmz'
    allowed_domains = ['dmz.org']
    start_urls = ['www.cnn.com']
    #rules = [Rule(SgmlLinkExtractor(allow=['/tor/\d+']), 'parse_torrent')]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]
    """