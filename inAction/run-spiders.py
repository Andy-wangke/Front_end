import scrapy
from scrapy.crawler import Crawler,CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
from scrapy import signals
from scrapy.utils.log import configure_logging
#import spiders
from spiders.stcn_stock import StcnStockSpider


options = {
    #'CONCURRENT_ITEMS': 250,
    #'USER_AGENT': 'Googlebot/2.1 (+http://www.google.com/bot.html)',
    #'CONCURRENT_REQUESTS': 30,
    'DOWNLOAD_DELAY': 3,
    #'COOKIES_ENABLED': False,
    }

settings = get_project_settings()
configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
settings.update(options);

#StcnStockSpider
runner = CrawlerRunner(settings)
runner.crawl(StcnStockSpider())


reactor.run()

