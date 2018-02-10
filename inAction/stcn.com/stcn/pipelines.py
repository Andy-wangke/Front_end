# -*- coding: utf-8 -*-
import json
import os
import logging
import codecs
import re
from scrapy import signals
from collections import OrderedDict

from datetime import datetime,timedelta

from stcn.my_settings import source_folder,test_mode,difference_days,source_pretty_folder,current_date,yester_date
from common.utils.mail import send

logger = logging.getLogger(__name__)

source_yester_name = source_folder+'stcn_'+yester_date+'.json'
source_current_name = source_folder+'stcn_'+current_date+'.json'

current_timestamp = datetime.today().strftime('%Y%m%d%H%M%S')
source_pretty_output= source_pretty_folder+ 'stcn_'+current_timestamp+'.json'



# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class JsonWithEncodingPipeline(object):


    @classmethod
    def from_crawler(cls,crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened,signals.spider_opened)

    '''
        1.check the file 
        2.duplicate filter
        3.insert data into file
    '''
    #Note:if the original file is empty,then need to instantiate file firstly
    def __init__(self):
        #try:
            #self.source_yester_file = codecs.open(source_yester_name,'r+',encoding ='utf-8')
            #self.source_current_file = codecs.open(source_current_name,'r+',encoding ='utf-8')

            #self.source_yester_output = codecs.open(source_yester_name,'a+',encoding ='utf-8')
            #self.origin_yester_items = json.load(codecs.open(source_yester_name,'r+',encoding = 'utf-8'))#raise json.decoder.JSONDecodeError
            #self.origin_yester_items = json.load(self.source_yester_output)
            #self.source_current_output = codecs.open(source_current_name,'a+',encoding ='utf-8')
            #self.origin_current_items = json.load(codecs.open(source_current_name,'r+',encoding = 'utf-8'))
            #self.origin_current_items = json.load(self.source_current_output)
            if test_mode:
                self.file_pretty_format = codecs.open(source_pretty_output,'a+',encoding ='utf-8')
        #except ValueError as e:
        #    print('Error({})'.format(e))

    #processing each item
    def process_item(self, item, spider):

        #import pdb;pdb.set_trace()
        try:
            try:
                self.source_yester_file = codecs.open(source_yester_name,'r+',encoding ='utf-8')
            except:
                self.source_yester_file = codecs.open(source_yester_name,'w',encoding ='utf-8')

            try:
                self.source_current_file = codecs.open(source_current_name,'r+',encoding ='utf-8')
            except:
                self.source_current_file = codecs.open(source_current_name,'w',encoding ='utf-8')
            #TODO:match more general
            item_publish_date = re.match(r'\d{4}\-\d{1,2}\-\d{1,2}',item['source'][0]).group(0)
            logger.info(">>>>>>>>>process spider %s,item:%s %s",spider.name,str(item['title']),item_publish_date)
            if yester_date == item_publish_date:#rewriting to the entire file instead of append to yesterday file
                self.check_save_into_file2(item,self.source_yester_file)
            elif current_date == item_publish_date:#rewriting to the entire file instead of append to current file
                self.check_save_into_file2(item,self.source_current_file)
            else:
                logger.debug(item_publish_date,"not in",[yester_date,current_date])
                
            if test_mode:
                line=json.dumps(OrderedDict(item),ensure_ascii = False,indent=4,sort_keys = False)+"\n"
                self.file_pretty_format.write(line)
        finally:
            self.source_yester_file.close()
            self.source_current_file.close()

        return item

    def check_save_into_file2(self,item,source_file):
        try:
            origin_items = json.load(source_file)
        except ValueError:
            logger.warning('source_file is not exist or is not a valid json object',)
            origin_items = []

        possible = [origin_item for origin_item in origin_items if origin_item['url'] == item['url']]
        if len(possible) >0:
            logger.warning("title:%s has existed in dataset.",item['title'])
        elif len(possible) == 0:
            #update the original dictionary list
            origin_items.append(OrderedDict(item))
            #Ref https://stackoverflow.com/questions/13949637/how-to-update-json-file-with-python
            source_file.seek(0) #rewind(move the cursor back to the beginning of the file then start writing)
            json.dump(origin_items,source_file,ensure_ascii = False,sort_keys = False)
            source_file.truncate() #deal with the case where the new data is smaller than the previous
        else:
            logger.warning("to be checking %s",str(item))

    # dropping duplicate and merge to file
    def check_save_into_file(self,item,origin_items,source_output_dict):
        possible = [origin_item for origin_item in origin_items if origin_item['url'] == item['url']]
        if len(possible) >0:
            logger.warning("title:%s has existed in dataset.",item['title'])
        elif len(possible) == 0:
            #append to file
            
            source_output_dict.update(item)
            json.dump(OrderedDict(item),source_output_dict,ensure_ascii = False,sort_keys = False)
            if test_mode:
                line=json.dumps(OrderedDict(item),ensure_ascii = False,indent=4,sort_keys = False)+"\n"
                self.file_pretty_format.write(line)
        else:
            logger.warning("to be checking %s",str(item))

    #when the spider is opened
    def open_spider(self,spider):
        logger.info(">>>>>>>open_spider event fired.....name=%s at %s",spider.name,datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        

    #when the spider is closed.
    def close_spider(self,spider):
        logger.info(">>>>>>>>close_spider event fired.....name=%s at %s",spider.name,datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        #TODO: close file
        msg = 'crawl finished'
        send(msg,"[AutoRun]scrapy spider","scrapy@hpe.com",['ke.wang@hpe.com'],'smtp3.hpe.com')
        if test_mode:
            self.file_pretty_format.close()
        #self.source_yester_output.close()
        #self.source_current_output.close()


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
        logger.info(">>>>>>>>>process spider %s",spider.name)


# integrated with Mongo
class MongoPipeline(object):
    #when the spider is opened
    def open_spider(self,spider):
        logger.info(">>>>>>>open_spider event fired.....name=%s at %s",spider.name,datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    #when the spider is closed.
    def close_spider(self,spider):
        logger.info(">>>>>>>>close_spider event fired.....name=%s at %s",spider.name,datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        #TODO: close file


    #processing each item
    def process_item(self, item, spider):
        logger.info(">>>>>>>>>process spider %s",spider.name)