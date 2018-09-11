#! python3

# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request

import logging
import json
import os
import re
import pprint
from datetime import datetime,timedelta

from  stcn.my_settings import subscribe_folder,test_mode,difference_days
from stcn.items import StcnItem


logger = logging.getLogger(__name__)
date_format='%Y%m%d'
current_date = datetime.today().strftime('%Y-%m-%d')

if not test_mode:
    # Note: default check the last one day data cause pretending it is a daily job
    yester_date = (datetime.today()- timedelta(days = difference_days)).strftime('%Y-%m-%d')

name_output = subscribe_folder+'stcn_title'+current_date+'.txt'
try:
    file_output=open(name_output,'a+',encoding='utf-8')
    title_in_file = open(name_output,'r',encoding='utf-8').readlines()
except ValueError as e:
    # TODO
    print("({})".format(e))

print("classpath:"+os.path.realpath(__file__))

options={}



class StcnStockSpider(CrawlSpider):
    name = 'stcn_stock'
    allowed_domains = ['stcn.com']
    start_urls = ['http://kuaixun.stcn.com/']

    rules = (
        Rule(LinkExtractor(allow=('index.shtml')), callback='parse_item'),
        Rule(LinkExtractor(allow=('index\.*?'),restrict_css=('ul a.next',)), callback='parse_item', follow=False),
    )

    def __init__(self,start_url='',*args,**kwargs):
        if start_url:
            self.start_urls=[start_url]
        super(StcnStockSpider,self).__init__(*args,**kwargs)

    def parse_item(self, response):
        print('current.response.url:'+response.url)
        selector=Selector(response)
        
        dates=selector.xpath('//div[@id="mainlist"]/ul/li/p/span/text()').re('(\d{4}\-\d{1,2}\-\d{1,2} \d{1,2}\:\d{1,2}\:\d{1,2})')
        #categorys=response.selector.xpath('//div[@id="mainlist"]/ul/li/p/a[@class="a1"]/text()').extract()
        #titles=response.selector.xpath('//div[@id="mainlist"]/ul/li/p/a[not(contains(@class,"a1"))]/text()').extract().strip()
        #urls=response.selector.xpath('//div[@id="mainlist"]/ul/li/p/a[not(contains(@class,"a1"))]/@href').extract()
        logger.info("dates.len:"+str(len(dates)))
        if len(dates) > 0 :
             stcnItems=[]
             for i in range(1,len(dates)+1):
                 #remove parenthese
                 #date = re.sub('\[(.*?)\]',r'\1',dates[i])
                 
                 category=selector.xpath('//div[@id="mainlist"]/ul/li[{0}]/p/a[@class="a1"]/text()'.format(str(i))).extract_first()
                 title=selector.xpath('//div[@id="mainlist"]/ul/li[{0}]/p/a[not(contains(@class,"a1"))]/text()'.format(str(i))).extract_first()
                 url =selector.xpath('//div[@id="mainlist"]/ul/li[{0}]/p/a[not(contains(@class,"a1"))]/@href'.format(str(i))).extract_first()
                 
                 category = re.sub('\【(.*?)\】',r'\1',category)
                 
                 stcnItem=StcnItem()
                 stcnItem['date'] = dates[i-1]
                 stcnItem['title'] = title
                 stcnItem['category'] = category
                 stcnItem['url'] = url
                 stcnItems.append(stcnItem)
                 yield Request(url,callback =self.parse_detail_page)
                 #import pdb; pdb.set_trace()
                 if current_date==re.split(r' ',dates[i-1])[0].strip():
                     #self.parse_update_data()
                     #items_dict=json.load(file_output)
                     if title +"\n" not in title_in_file:
                         file_output.write(title+"\n")
                         print("Spider: stcn_stock.title {0} added to file".format(title))
                     else:
                         print("Spider: stcn_stock.title {0} already in the file".format(title))
        else:
            logger.warning('the date.len is 0')



    def parse_detail_page(self,response):
        print(response.url)



