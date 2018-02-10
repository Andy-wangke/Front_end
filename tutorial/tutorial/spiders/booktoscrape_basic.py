 # -*- coding: utf-8 -*-
import scrapy

from scrapy.http import Request
from urllib.parse import urlparse

#forked from https://github.com/stummjr/books_crawler/
class BookToscrapeSpider(scrapy.Spider):
    name = 'booktoscrape'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    count = 0
    #first scrape the first page
    #goto next page and scraping
    def parse(self, response):
        for book_url in response.css('article.product_pod >h3 > a ::attr(href)').extract():
            yield Request(response.urljoin(book_url),meta={'deltafetch_key':urlparse(book_url).path.split('/')[-2]},callback=self.parse_book_page)
        #go to next page
        next_page=response.css('li.next > a ::attr(href)').extract_first()
        if next_page:
            if self.count <1:
                self.count = self.count+1
                yield Request(response.urljoin(next_page),callback = self.parse)

    def parse_book_page(self,response):
        item={}
        product = response.css('div.product_main')
        item['title'] = product.css('h1 ::text').extract_first()
        item['category'] = response.xpath(
            "//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()"
            ).extract_first()
        yield item
        
