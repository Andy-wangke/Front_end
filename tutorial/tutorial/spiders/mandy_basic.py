# -*- coding: utf-8 -*-
import scrapy

print("hello world")

class MandySpider(scrapy.Spider):
    name = 'mandy'
    allowed_domains = ['mandy.com']
    start_urls = ['http://mandy.com/']

    def parse(self, response):
        pass




