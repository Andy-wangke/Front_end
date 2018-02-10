# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
import logging
import math
import json
import pprint

from common.common_spider import CommonSpider
from sinafinance.items import SinaItem

logger = logging.getLogger(__name__)


#custom
item_num=50
pages=1
        

class SinaFinanceSpider(Spider):
    '''
        http://feed.mix.sina.com.cn/api/roll/get?pageid=205&lid=1789&num=10&page=2&callback=feedCardJsonpCallback
        http://feed.mix.sina.com.cn/api/roll/get?pageid=205&lid=1789&num=10&page=1&type=jsonp
        
        @pageid :

        @lid : 
        @num : items num of single page.
                        max:50
        @page : the page number

        @type: data format
    '''
    name = 'sina_financeV2'
    allowed_domains = ['sina.com.cn']
    #
    start_urls = ['http://finance.sina.com.cn/stock/newstock/']

    all_css_rules={
        'div.wrap-inner':{
            'title':'div.page-header h1#artibodyTitle::text',
            'info':'div.page-info span.time-source::text',
            'content':'div.page-content div.article p::text'

        }

    }

    def parse(self, response):
        #logger.info("SinaFinance : %s",response.body)

        url='http://feed.mix.sina.com.cn/api/roll/get?pageid=205&lid=1789&type=jsonp'
        yield Request(url,callback=self.parse_count_page)
    
    def parse_count_page(self,response):
        #TODO:if not return your target page by checking for logo name or other significant element
        #if not response.headers['status'] =200 :
         #   yield Request(url=response.url,dont_filter=True)
        try:
            rawdata=json.loads(response.body.decode('utf-8'))
        except ValueError as e:
            logger.error("parse data faliled. \n%s",e)
            
        headers={
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                        'Accept-Encoding': 'gzip, deflate',
                         'Host':'feed.mix.sina.com.cn',
                         'referer':'http://finance.sina.com.cn/stock/newstock/',
                         #'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
                 }
        if "succ" == rawdata["result"]["status"]["msg"]:
                item_count=rawdata["result"]["total"]
                if bool(item_count):      
                    pages=math.ceil(item_count/item_num)
                    logger.info("SinaFinance Feed page count: %s",pages)
                    for page in range(1,int(pages)+1):
                        yield FormRequest(url=response.url+'&num={}&page={}'.format(str(item_num),str(page)),headers=headers,callback=self.parse_data)

        
    def parse_data(self,response):
        rawdata=json.loads(response.body.decode('utf-8'))
        logger.info("'parse response data:\n %s \n %s"%(response.url,str(rawdata)))
        if rawdata :
            if "succ" == rawdata["result"]["status"]["msg"]:
                size =len(rawdata['result']['data'])#Fix the last page size issue
                for i in range(1,int(size)+1):
                    item_link=rawdata['result']['data'][i-1]['url']
                    yield Request(item_link,callback=self.parse_detail_page)

    def parse_detail_page(self,response):
        pass
        
        
