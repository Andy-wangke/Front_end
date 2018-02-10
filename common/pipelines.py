# -*- coding: utf-8 -*-

import os
import json
import logging

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


logger = logging.getLogger(__name__)

class JsonWithEncodingPipeline(object):

    def process_item(self, item, spider):
        return item

# integrated with Redis
class RedisPipeline(object):
    #when the spider is opened
    def open_spider(self,spider):
        logger.info(">>>>>>>open_spider event fired.....name=%s at %s",spider.name,datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    #when the spider is closed.
    def close_spider(self,spider):
        logger.info(">>>>>>>>close_spider event fired.....name=%s at %s",spider.name,datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        #TODO: close file
        
    #processing each item
    def process_item(self, item, spider):
        return item


# integrated with MongoDB
class MongoDBPipeline(object):
    import pymongo
    collection_items = 'scrapy_items'
    def __init__(self,mongo_uri,mongo_db):
        logger.info("init MongoDB pipeline....")
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        self.settings = crawler.settings
        return cls(
                mongo_uri = crawler.settings.get('MONGO_URI'),
                mongo_db = crawler.settings.get('MONGO_DB','items')
            )


    #when the spider is opened
    def open_spider(self,spider):
        logger.info(">>>>>>>open_mongodb Client fired.....name=%s at %s",spider.name,datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        #connect to mongodb server
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection_items]
        if self.__get_unique_key() is not None:
            self.collection.create_index(self.__get_unique_key(),unique = True)

    #when the spider is closed.
    def close_spider(self,spider):
        logger.info(">>>>>>>>close_mongodb event fired.....name=%s at %s",spider.name,datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        #TODO: close file
        self.client.close()


    #processing each item
    def process_item(self, item, spider):
        if self.__get_unique_key() is None:
            #insert
            self.collection.insert_one(dict(item))
        else:
            #update
            self.collection.update(
                    {self.__get_unique_key():item[self.__get_unique_key()]},
                    dict(item),
                    upsert = True
                )

        return item

    def __get_unique_key(self):
        if not self.settings['__get_unique_key'] or self.settings['__get_unique_key'] =='':
            return None
        return self.settings['__get_unique_key']


#TODO:unit test
class ScreenshotPipeline(object):
    import scrapy
    import hashlib
    from urllib.parse import quote
    '''
        Pipeline that uses Splash to render screenshot of every Scrapy Item that fire the issue.
        Ref https://doc.scrapy.org/en/latest/topics/item-pipeline.html?highlight=mongodb#take-screenshot-of-item
    '''
    SPLASH_URL = "http://localhost:8050/render.png?url={}"
    def process_item(self,item,spider):
        if item['url']:
            encoded_item_url=quote(item['url'])
            screenshot_url = self.SPLASH_URL.format(encoded_item_url)
            request = scrapy.Request(screenshot_url)
            dfd  =spider.crawler.engine.download(request,spider)
            dfd.addBoth(self.return_item,item)#what this mean?
            return dfd

    def return_item(self,response,item):
        if response.status !=200:
            #error happened,return item
            return item

        #save screenshot to file,filename will be hash of url
        url = item["url"]
        url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        filename = "{}.png".format(url_hash)

        with open(filename,'wb') as f:
            f.write(response.body)

        #Store filename in item
        item['screenshot_filename'] = filename
        return item