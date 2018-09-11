# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging

logger=logging.getLogger(__name__)


class StackoverflowSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class StackoverflowDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


from scrapy.downloadermiddlewares.retry import RetryMiddleware
from datetime import datetime,timedelta

counter_file='counter_record.txt'
current_counter_session=[]#counter stored in current session
file_append=open(counter_file,'a',encoding='utf-8')
try:
    counter_in_file=open(counter_file,'r').readlines()
except:
    counter_in_file=open(counter_file,'w')

class ClockInCounterRetryMiddleware(RetryMiddleware):

    #TODO close file 
    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        #save into file and compare with previous day counter and retry
        if response.status ==200 and response.selector.css(spider.counter_css_path).extract_first():
            counter=response.selector.css(spider.counter_css_path).extract_first()
            current_timeframe=datetime.today().strftime('%Y-%m-%d')
            yesterday_timeframe=datetime.strftime(datetime.now()-timedelta(1),'%Y-%m-%d')
            logger.info('current day counter is %s'%counter)
            if current_timeframe+' '+counter+'\n' not in counter_in_file:
                file_append.write(current_timeframe+' '+counter+'\n')
            elif len(counter_in_file)>1 and yesterday_timeframe in counter_in_file[-2] and yesterday_timeframe+' '+(str(int(counter.split('/')[0])-1)+'/'+counter.split('/')[1])+'\n' not in counter_in_file:#counter_in_file[-1]
                    #compare last line to check whether counter same as previous day
                    return self._retry(request,'counter same as previous day,thus retry...{}'.format(counter), spider) or response
        return response

    def process_exception(self, request, exception, spider):
    # Called when a download handler or a process_request()
    # (from other downloader middleware) raises an exception.

    # Must either:
    # - return None: continue processing this exception
    # - return a Response object: stops process_exception() chain
    # - return a Request object: stops process_exception() chain
        counter_in_file.close()
        file_append.close()