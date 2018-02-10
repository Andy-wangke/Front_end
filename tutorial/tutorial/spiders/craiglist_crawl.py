# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request

import logging as log
import re

#settings
keyword = ["feature film", "indie film", "film production", "independent film", "film casting", "movie casting",
           "extras casting", "film editor", "movie editor", "post production", "movie production", "line producer",
           "production manager", "editor", "colorist", "visual effects", "sound design", "VFX", "motion picture",
           "film sales", "film distribution", "film budget"]

name_file = 'outfile.txt'

test_mode = True  # True or False
difference_days = 2 # Test mode

print('init spider Craiglist')

class CraiglistSpider(Spider):
    name = 'craiglist'
    allowed_domains = ['craiglist.org']
    start_urls = ['http://craiglist.org/']

    def parse(self, response):
        log.info('parse method is invoked...')
        #pass
