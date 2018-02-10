# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
import logging as log

from tutorial.my_settings import keyword,name_file

import re

#custom settings


#processing(replace ' ' to '%20')
keyword = list(map(lambda x: re.sub(' ','%20',x),keyword))



print('Init spider ProductionHub...')



class ProductionhubSpider(Spider):
    name = 'productionhub'
    allowed_domains = ['productionhub.com']
    start_urls = ['http://www.productionhub.com/jobs/search?q={}'.format(key)
                                for key in keyword]
    

    def parse(self, response):
        sel=Selector(response)
        #note:xpath element array start with 1 instead of 0

        #count = sel.xpath('//*[@id="main-content"]/div[3]/div/text()').re('\w+')
        #match and fetch job counts
        count=sel.xpath('//*[@id="main-content"]/div/div/div/text()').re('\d+');#return a list
        log.info('before bool the job count is %s',count)
        if bool(count):
            log.info('before the job count is %s',count)
            count = count[-1]
            log.info('after the job count is %s',count)
            for num_page in range(1,int(count)+1):
                pass
                #yield Request

    def parse_count_page(self,response):
        pass
        
