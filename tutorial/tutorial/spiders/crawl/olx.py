# -*- coding: utf-8 -*-
# ref  https://medium.com/python-pandemonium/develop-your-first-web-crawler-in-python-scrapy-6b2ee4baf954
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tutorial.items  import OlxItem
import logging


class OlxSpider(CrawlSpider):
    name = 'olx'
    allowed_domains = ['www.olx.com.pk']
    start_urls = [
        'https://www.olx.com.pk/computers-accessories/',
        #'https://www.olx.com.pk/tv-video-audio/',
        #'https://www.olx.com.pk/games-entertainment/'
                  ]

    rules = (
        Rule(LinkExtractor(allow='', restrict_css=('.pageNextPrev',)),callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        print('Processing..' +response.url)
        logging.warning("This is a warning")
        item_links=response.css('.large > .detailsLink::attr(href)').extract()

        for a in item_links:
            yield scrapy.Request(a,callback=self.parse_detail_page)
        #i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        #return i

    def parse_detail_page(self,response):
        title = response.css('h1::text').extract()[0].strip()
        price = response.css('.pricelabel > strong::text').extract()[0]

        item = OlxItem()
        item['title'] = title
        item['price'] = price
        item['url'] = response.url
        #iterator function 
        yield item
        
