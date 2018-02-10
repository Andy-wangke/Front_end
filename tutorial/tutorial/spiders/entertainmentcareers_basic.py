# -*- coding: utf-8 -*-
import scrapy
import re
import pprint
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.crawler import Crawler,CrawlerRunner
from datetime import datetime
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
#from scrapy import log
#from tutorial.my_settings import keyword,name_file


#custom setting
keyword = ["feature film", "indie film", "film production", "independent film", "film casting", "movie casting",
           "extras casting", "film editor", "movie editor", "post production", "movie production", "line producer",
           "production manager", "editor", "colorist", "visual effects", "sound design", "VFX", "motion picture",
           "film sales", "film distribution", "film budget"]


# options = {
#         'CONCURRENT_ITEMS': 150,
#         'USER_AGENT': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) "
#                       "Chrome/19.0.1055.1 Safari/535.24",
#         'CONCURRENT_REQUESTS': 5,
#         'SW_SAVE_BUFFER': 30,
#         'DOWNLOAD_DELAY': 1.5,
#         'COOKIES_ENABLED': False,
#     }
name_file = '../outfile.txt'

#processing
keyword = list(map(lambda x :re.sub(' ','+',x),keyword))
print("keyword:"+str(keyword))

file =open (name_file,'a')

email_in_file = open(name_file,'r').readlines()


class EntertainmentcareersSpider(Spider):
    name = 'entertainmentcareers'
    allowed_domains = ['entertainmentcareers.net']
    
    start_urls = ['http://www.entertainmentcareers.net/psearch/?zoom_query={}'.format(key)
                              for key in keyword]

    def parse(self, response):
        sel = Selector(response)

        links=sel.xpath('//*[@class = "result_title"]/a/@href').extract()
        pprint.pprint(links)

        for link in links:
            yield Request(url=link,callback=self.parse_detail_page)


    def parse_detail_page(self,response):
        print(response.url)
        sel = Selector(response)
        
        
        pass

def run():
    options = {
        'CONCURRENT_ITEMS': 250,
        #'USER_AGENT': 'Googlebot/2.1 (+http://www.google.com/bot.html)',
        'CONCURRENT_REQUESTS': 30,
        'DOWNLOAD_DELAY': 0.5,
        'COOKIES_ENABLED': False,
        }

    spider = EntertainmentcareersSpider()

    settings = get_project_settings()
    settings.update(options)

    runner= CrawlerRunner(settings)
    runner.crawl(spider)

    d= runner.join()
    d.addBoth(lambda _:reactor.stop())
    #crawler = Crawler(settings)
    #crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    #crawler.install()
    #crawler.configure()
    #crawler.crawl(spider)
    #crawler.start()
    #log.start(logfile="results.log", loglevel=log.DEBUG, crawler=crawler, logstdout=False)
    reactor.run()



if __name__ == '__main__':
    run()
        
        
        
