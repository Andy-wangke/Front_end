# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import logging


class FundingSpider(CrawlSpider):
    '''
        this is the spider for NetEase
    '''
    name = 'funding'
    allowed_domains = ['www.163.com']
    start_urls = [
        'http://money.163.com/stock/',
        #'http://money.163.com/hkstock/',
        #'http://money.163.com/usstock/',
        #'http://money.163.com/ipo/'
                  ]

    rules = (
        Rule(LinkExtractor(allow='',restrict_css=('.load_more_btn',)), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        #fetch all links
        item_links = response.css(' .news_article .news_title > h3 > a::attr(href)').extract()
        print('items_links -->'+item_links)
        print('items_links.length '+len(item_links))
        #for a in item_links:
            #yield scrapy.Request(a,callback=self.parse_detail_page)
        #i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        
        #return i
            
    def parse_detail_page(self,response):
        pass
        #response.css('')
        
            

