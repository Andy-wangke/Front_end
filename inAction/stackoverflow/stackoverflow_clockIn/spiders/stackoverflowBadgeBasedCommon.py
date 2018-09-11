# -*- coding: utf-8 -*-
#! python3
#stackOverflowBadge.py call startoverflow via curl

import scrapy
import logging
import urllib.request
from scrapy.spiders import CrawlSpider
# from common.utils.mail import send
from common.common_spider import CommonSpider

logger=logging.getLogger(__name__)


STACKOVERFLOW_SELF_URL='https://stackoverflow.com/users/6891192/andywang';


def call():
    urllib.request.urlopen(STACKOVERFLOW_SELF_URL)


class StackOverflowBadgeBasedCommon(CrawlSpider):
    '''
        Scrapes login badge count to record and compare with the previous day(counted in UTC),if count+1,then finish,otherwise,retry
        How to retry?
            1.retry spider
            2.retry by scheduler(set seperate time)
        multiThread

    '''
    name = "SO_Login_Badge"
    allowed_domains = ['www.stackoverflow.com']
    start_urls = ['https://stackoverflow.com/users/6891192/andywang?tab=reputation'] 

    def start_requests(self):
        urls=[
            'https://www.coursetalk.com/subjects/data-science/courses/'
        ]
        # headers={
        #     'User-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        #     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        #     'Accept-encoding':'gzip, deflate, br',
        #     'Accept-language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        # }
        for url in urls:
            yield scrapy.Request(url = url,callback=self.parse)



    def parse(self, response):
        logging.info("response.status:%s"%response.status)
        #logging.info("response.body:%s"%response.body)
        logourl = response.selector.css('div.main-nav__logo img').xpath('@src').extract()
        logging.info('response.logourl:%s'%logourl)