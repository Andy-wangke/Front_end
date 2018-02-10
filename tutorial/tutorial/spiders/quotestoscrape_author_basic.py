
import scrapy

class AuthorSpider(scrapy.Spider):
    name='author'

    start_urls=['http://quotes.toscrape.com/']

    def parse(self,response):
        #follow links to author pages
        for href in response.css('.author +a::attr(href)'):
            yield response.follow(href,self.parse_author)

        #follow pagination links
        #for href in 
