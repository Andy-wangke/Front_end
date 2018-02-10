#import module firstly
import sys
import os
from os.path import dirname
path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(path)
sys.path.append(dirname(path))
print('current path:%s,%s'% (path,dirname(path)))


import scrapy
from scrapy.crawler import Crawler,CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
from scrapy import signals
from scrapy.utils.log import configure_logging


#run spider from script
def run_spider():
	options = {
	    'CONCURRENT_ITEMS': 250,
	    'USER_AGENT': 'Googlebot/2.1 (+http://www.google.com/bot.html)',
	    'CONCURRENT_REQUESTS': 30,
	    'DOWNLOAD_DELAY': 0.5,
	    'COOKIES_ENABLED': False,
	    }

	settings = get_project_settings()
	configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
	settings.update(options);

	#BookToscrapeSpider basic version
	from tutorial.spiders.booktoscrape_basic import BookToscrapeSpider
	#runner = CrawlerRunner(settings)
	#runner.crawl(BookToscrapeSpider())

	#BookToscrapeSpider crawl version
	from tutorial.spiders.booktoscrape_crawl import BookToscrapeSpider as BookToscrapeSpider_crawl
	runner = CrawlerRunner(settings)
	runner.crawl(BookToscrapeSpider_crawl())

    #crawler = Crawler(settings)
    #crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    #crawler.install()
    #crawler.configure()
    #crawler.crawl(spider)
    #crawler.start()
    #log.start(logfile="results.log", loglevel=log.DEBUG, crawler=crawler, logstdout=False)
	d= runner.join()
	d.addBoth(lambda _:reactor.stop())

	reactor.run()

if __name__ == '__main__':
    run_spider()