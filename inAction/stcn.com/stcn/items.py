# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BaseItem(scrapy.Item):
    url = scrapy.Field()
    domain = scrapy.Field()
    timestamp = scrapy.Field()
    status = scrapy.Field()

class StcnItem(BaseItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    url = scrapy.Field()
    category=scrapy.Field()
    date=scrapy.Field(serializer=str)

class StcnDetailItem(BaseItem):
    category  = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()
    content  = scrapy.Field()
