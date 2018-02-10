
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class MyCrawlSpider(CrawlSpider):
    name='crawlSpider'
    allowed_domains=['toscrape.com']

    start_urls=['http://quotes.toscrape.com']

    #rules=(
        #
        #
       #Rule(LinkExtractor(allow=('category\.php',)))


       # )

    def parse_item(self,response):
        self.logger.info('Hi, this is an item page! %s',response.url)
        item=scrapy.Item()
        
    
