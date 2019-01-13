# -*- coding: utf-8 -*-
import scrapy

from scrapy.mail import MailSender
from scrapy.utils.project import get_project_settings 

settings = get_project_settings()

class RedditbotSpider(scrapy.Spider):
    name = 'redditbot'
    allowed_domains = ['www.reddit.com/r/gameofthrones/']
    start_urls = ['http://www.reddit.com/r/gameofthrones//']



    #mailer =MailSender()

    def parse(self, response):
    	mailer = MailSender.from_settings(settings)
    	try:
        	mailer.send(to=["test@test.com"],subject="scrapy spider",body="test message",cc=['test@test.com'],charset="utf-8")
    	except Exception as e :
        	msg = "Error occurred...{0}".format(str(e))
        	print(msg)


    	print('mail sending')



