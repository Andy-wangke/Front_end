# -*- coding: utf-8 -*-

import sys
import os
from os.path import dirname
path = dirname(dirname(os.path.abspath(os.path.dirname(__file__))))
# print('current path:%s'% path)
sys.path.append(path)
sys.path.append(dirname(path))
#print('sys path:%s'% sys.path)

# Scrapy settings for stackoverflow_clockIn project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'stackoverflow_clockIn'

SPIDER_MODULES = ['stackoverflow_clockIn.spiders']
NEWSPIDER_MODULE = 'stackoverflow_clockIn.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'stackoverflow_clockIn (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 1
#CONCURRENT_REQUESTS_PER_IP = 16

REDIRECT_ENABLED = True
# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#       #incremental or delta policy to fetch source data
# #    'stcn.middlewares.TutorialSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
      'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
      'stackoverflow_clockIn.middlewares.ClockInCounterRetryMiddleware':90,
      'scrapy_proxies.RandomProxy' : 100,
      'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
#    'stcn.middlewares.StcnSpiderMiddleware': 543,

      'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
      'common.middlewares.RandomUserAgentMiddleware': 400,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'stackoverflow.pipelines.StackoverflowPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 600
HTTPCACHE_DIR = '/stcnhttpcache/'
#don't cache response with these http codes
HTTPCACHE_IGNORE_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# requests not found in the cache will be ignored instead of downloaded
HTTPCACHE_IGNORE_MISSING = True
#don't cache responses with these URI schemes
HTTPCACHE_IGNORE_SCHEMES = ['file']
HTTPCACHE_POLICY= 'scrapy.extensions.httpcache.DummyPolicy'

#Log
LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FILE = 'scrapy.log'
LOG_LEVEL='DEBUG'


#Retry
RETRY_ENABLED=True
#Retry many times since proxies often fail
RETRY_TIMES=2
#Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES=[500, 503, 504, 400, 403, 404, 408]

#custom scrapy proxies
# Proxy mode
# 0 = Every requests have different proxy
# 1 = Take only one proxy from the list and assign it to every requests
# 2 = Put a custom proxy to use in the settings
PROXY_MODE = 0
# Proxy list containing entries like
# http://host1:port
# http://username:password@host2:port
# http://host3:port
# ...P
PROXY_LIST = path+'\\proxy_pool.txt'
#if proxy mode is 2 ,then uncomment this line
#CUSTOM_PROXY = "http://usr:pwd@hostname:port"