# -*- coding: utf-8 -*-
#! python3
#stackOverflowBadge.py call startoverflow via curl

import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.item import Item,Field
from scrapy.http import Request,FormRequest
import logging
import urllib.request
import base64
from datetime import datetime

from common.utils.mail import sendeBay

logger=logging.getLogger(__name__)


STACKOVERFLOW_SELF_URL='https://stackoverflow.com/users/6891192/andywang?tab=topactivity'

# def call():
#     urllib.request.urlopen(STACKOVERFLOW_SELF_URL)



class SOBadgeCounter(scrapy.Spider):
    '''
        Scrapes login badge count to record and compare with the previous day(counted in UTC),if count+1,then finish,otherwise,retry by open the window
        0.spider
            stackoverflow login and visit my SO profile page,
            then grabbing the fanatic badge progress and sending it by mail daily

        1.How to retry?
            1.retry spider
            2.retry by scheduler(set seperate time)
        2.multiThread
        3.send email notification while success/failed

        we can verify the consecutive day counter by this dev api(https://api.stackexchange.com/docs)

    '''
    name = 'SO_Badge_counter'
    allowed_domains = ['stackoverflow.com']
    #start_urls = ['https://stackoverflow.com/users/6891192/andywang?tab=reputation'] 
    #counter=0
    counter_css_path='div#top-cards aside.-badges span.-count::text'

    # fill post forms and login
    def start_requests(self):
        urls=[
            'https://stackoverflow.com/users/login-add?ssrc=head&returnurl=https%3a%2f%2fstackoverflow.com%2fusers%2f6891192%2fandywang'
        ]
        # headers={
        #     'User-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        #     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        #     'Accept-encoding':'gzip, deflate, br',
        #     'Accept-language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        # }

        #encoded=base64.b64encode(bytes('pwd','utf-8'))
        for url in urls:
            yield FormRequest(url = url,formdata={'email':'andy_wang_ke@163.com','password':base64.b64decode(b'd2FuZ2tlODE5OTQwNTMw').decode('utf-8')},
                            callback=self.after_login)


    def after_login(self,response):
        logging.info("login status:%s"%response.status)
        #logging.info(response.text)
        if 'The email or password is incorrect' in response.text:
            logging.error("Login failed...:(")
            # TODO retry
            current_timeframe=datetime.now().strftime('%Y-%m-%d %H:%M')
            msg='StackOverflow login failed reminder,current date in UTC+8 {0},please check login progress'.format(current_timeframe)
            sendeBay(msg,'[REMINDER]Stackoverflow AutoRun!!')
            return
        else:
            logging.info("authentication success.:)")
            return Request(url=STACKOVERFLOW_SELF_URL,callback=self.fetch_badges_info,dont_filter=True)


    #grabbing the fanatic badge progress,then sending email for notification    
    def fetch_badges_info(self, response):
        logging.info("response.status:%s"%response.status)
        counter = response.selector.css(self.counter_css_path).extract()
        logging.info('response.badge.counter:%s'%counter)
        current_timeframe=datetime.now().strftime('%Y-%m-%d %H:%M')
        msg='StackOverflow login count reminder,current date in UTC+8 {0} badge counter is {1}'.format(current_timeframe,counter[0])
        sendeBay(msg,'[REMINDER]Stackoverflow AutoRun!!!')

    def send_reminder(msg):
        pass
