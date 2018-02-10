# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request

from stcn.my_settings import subscribe_folder,test_mode,difference_days,yester_date,current_date
from stcn.items import StcnItem,StcnDetailItem
from common.common_spider import CommonSpider
from common.utils.mail import send

import logging
import json
import os
import re
import pprint
from datetime import datetime,timedelta
from scrapy.mail import MailSender

from urllib.parse import urlparse

logger = logging.getLogger(__name__)

#date_format='%Y-%m-%d'
#if test_mode:
#    current_date = datetime.today().strftime(date_format)
#else:# Note: default check the last one day data cause pretending it is a daily job
#current_date = datetime.today().strftime('%Y-%m-%d')
#yester_date = (datetime.today()- timedelta(days = difference_days)).strftime('%Y-%m-%d')
# check the last and current date
try:
    check_date = [yester_date,current_date]
except NameError:
    check_date = [current_date]

    
name_output = subscribe_folder+'stcn_title'+current_date+'.txt'
try:
    file_output=open(name_output,'a+',encoding='utf-8')
    title_in_file = open(name_output,'r',encoding='utf-8').readlines()
except ValueError as e:
    # TODO
    logger.error("File Error({})".format(e))

print("classpath:"+os.path.realpath(__file__))



class StcnStockSpider(CommonSpider):
    '''
    save data into json file by pipeline



    '''
    name = 'stcn_stock2'
    allowed_domains = ['stcn.com']
    start_urls = ['http://kuaixun.stcn.com/']

    rules = (
        Rule(LinkExtractor(allow=('index.shtml')), callback='parse_item'),
        Rule(LinkExtractor(allow=('index\.*?'),restrict_css=('ul a.next',)), callback='parse_item', follow=True),
    )
    item_css_rules={
        'div.content':{
            '__use':'dump',
            '__list':True,
            'category':'div.website a:last-child::text',
            'title':'div.intal_tit h2::text',
            'source':'div.intal_tit div.info *::text',
            'content':'div.txt_con *::text',
            }
    }

    #mailer = MailSender()

    def __init__(self,start_url='',*args,**kwargs):
        if start_url:
            self.start_urls=[start_url]
        super(StcnStockSpider,self).__init__(*args,**kwargs)

        
    def parse_item(self, response):
        print('current.response.url for page:'+response.url)
        selector=Selector(response)
        
        dates=selector.xpath('//div[@id="mainlist"]/ul/li/p/span/text()').re('(\d{4}\-\d{1,2}\-\d{1,2} \d{1,2}\:\d{1,2}\:\d{1,2})')

        try:
            if len(dates) > 0 :
                stcnItems=[]
                for i in range(1,len(dates)+1):
                    category = selector.xpath('//div[@id="mainlist"]/ul/li[{0}]/p/a[@class="a1"]/text()'.format(str(i))).extract_first()
                    title = selector.xpath('//div[@id="mainlist"]/ul/li[{0}]/p/a[not(contains(@class,"a1"))]/text()'.format(str(i))).extract_first()
                    url = selector.xpath('//div[@id="mainlist"]/ul/li[{0}]/p/a[not(contains(@class,"a1"))]/@href'.format(str(i))).extract_first()

                    item_date = re.split(r' ',dates[i-1])[0].strip()
                    if item_date in check_date:
                        #import pdb;pdb.set_trace()
                        deltafetch_key=urlparse(url).path.split('.')[0]
                        yield Request(url,meta={'deltafetch_key':deltafetch_key},callback =self.parse_detail_page)
                        #self.parse_update_data()
                        #items_dict=json.load(file_output)
                        if title +"\n" not in title_in_file:
                            file_output.write(title+"\n")
                            print("Spider: stcn_stock.title {0} added to file".format(title))
                        else:
                            print("Spider: stcn_stock.title {0} already in the file".format(title))
            else:
                logger.warning('the date.len is 0')
        except Exception as e:
            msg = "Error occurred...{0}".format(e)
            logger.error(msg)
            send(msg,"[AutoRun]scrapy spider","scrapy@hpe.com",['ke.wang@hpe.com'],'smtp3.hpe.com')
            raise
        finally:
            #close the resources
            #file_output.close()
            #import pdb; pdb.set_trace()
            pass
            #mailer.send(to=["ke.wang@hpe.com"],subject="[AutoRun]scrapy spider",body="crawl finishing",cc=["ke.wang@hpe.com"])




    def parse_detail_page(self,response):
        #import pdb;pdb.set_trace()
        stcn_detail_item=self.parse_with_rules(response,self.item_css_rules,StcnDetailItem)
        if stcn_detail_item:
            #logger.info('stcn_detail_item:'+str(stcn_detail_item))
            #pprint.pprint(rule_item)
            return stcn_detail_item
