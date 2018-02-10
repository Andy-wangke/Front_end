# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from tutorial.my_settings import name_file,test_mode,difference_days
from datetime import datetime,timedelta


print('Init spider Newenglandfilm successfully')

file_output = open(name_file,'a')#mode 'a' means open for writing ,append to the end of the file if it exists
email_current_session = []
email_in_file = open(name_file,'r').readlines()#mode 'r' means open for reading (which is default value)


if test_mode:
    current_date=(datetime.today() - timedelta(days=difference_days)).strftime('%m/%d/%Y')
else:
    current_date= datetime.today().strftime('%m/%d/%Y')


class NewenglandfilmSpider(Spider):
    """
    fetch all address into file
    """
    name = 'newenglandFilm'
    
    allowed_domains = ['newenglandfilm.com']
    
    start_urls = ['https://newenglandfilm.com/classifieds/browse-all']

    def parse(self, response):
        sel=Selector(response)
        #TODO:check if return the information that you want,otherwise 
        for num_div in range(1,31):
            date=sel.xpath('//*[contains(@class,"main-content")]/div/div[@id="classiwrapper"]/div[contains(@class,"awpcp-listings")]/div[{0}]/div/p/text()'.format(str(num_div))).re('(\d{1,2}\/\d{1,2}\/\d{4})')[0]
            #date=sel.xpath('//*[contains(@class,"main-content")]/div/div[@id="classiwrapper"]/div/div[{0}]/div/p/text()'.format(str(num_div))).re('(\d{1,2}\/\d{1,2}\/\d{4})')[0]
            #email=sel.xpath('//*[contains(@class,"main-content")]/div/div[@id="classiwrapper"]/div[contains(@class,"awpcp-listings")]/div[1]/div/div/div/span/a/text()').re('(\w+@[a-zA-Z0-9_]+?\.[a-zA-Z]{2,6})')
            email=sel.xpath('//*[contains(@class,"main-content")]/div/div[@id="classiwrapper"]/div[contains(@class,"awpcp-listings")]/div[{0}]/div/div/div/span/a/text()'.format(str(num_div))).re('(\w+@[a-zA-Z0-9_]+?\.[a-zA-Z]{2,6})')
            if current_date == date:
                for address in email:
                    if address +"\n" not in email_in_file and address not in email_current_session:
                        file_output.write(address+'\n')
                        email_current_session.append(address)
                        print("Spider: NewenglandFilm. Email {0} added to file".format(address))
                    else:
                        print ("Spider: NewenglandFilm. Email {0} already in the file".format(address))
