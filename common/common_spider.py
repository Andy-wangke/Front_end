# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.item import BaseItem

import logging
import re
import json
#import pprint

logger = logging.getLogger(__name__)



class CommonSpider(CrawlSpider):
    ''' 
    # all css rule example:
    all_css_rules = {
        '.zm-profile-header': {
            '.zm-profile-header-main': {
                '__use':'dump',
                'name':'.title-section .name::text',
                'sign':'.title-section .bio::text',
                'location':'.location.item::text',
                'business':'.business.item::text',
                'employment':'.employment.item::text',
                'position':'.position.item::text',
                'education':'.education.item::text',
                'education_extra':'.education-extra.item::text',
            }, '.zm-profile-header-operation': {
                '__use':'dump',
                'agree':'.zm-profile-header-user-agree strong::text',
                'thanks':'.zm-profile-header-user-thanks strong::text',
            }, '.profile-navbar': {
                '__use':'dump',
                'asks':'a[href*=asks] .num::text',
                'answers':'a[href*=answers] .num::text',
                'posts':'a[href*=posts] .num::text',
                'collections':'a[href*=collections] .num::text',
                'logs':'a[href*=logs] .num::text',
            },
        }, '.zm-profile-side-following': {
            '__use':'dump',
            'followees':'a.item[href*=followees] strong::text',
            'followers':'a.item[href*=followers] strong::text',
        }
    }
    
    #all xpath rule example
    Note:
    #.// is relative of the superior node
    # // is absolute of the top node 
    all_xpath_rules={
        '//div[contains(@class,"product_main")]':{
                '__use':'dump',
                '__list':True,
                'title':'.//h1/text()',
                'category':'//ul[contains(@class,"breadcrumb")]/li[contains(@class,"active")]/preceding-sibling::li[1]/a/text()',
                'price':'.//p[contains(@class,"price_color")]/text()',
                'availability':'.//p[contains(@class,"availability")]/text()'
                #'description':''
            }
        }
    '''
    custom_settings={
        'DOWNLOAD_TIMEOUT':90
        }

    count = 0
    '''        
    #__use:[dump]
            if variable __use not exists, then loop nest,otherwise start parse
    #__list:boolean
                if variable __list exists or True,which means item field return a list,otherwise return the first value of array (array[0])
    #__sel:[css(default),xpath]
                if variable use css selector,then will parse rule by css,as applied to xpath


        Provide the common spider funtion
        if item_class is initial dict , then traverse 
        and if item_class is a subclass of dict(item),then traverse through corresponding item

        TODO:
        Done 1. add xpath rule template 
        Done by magic field middleware 2. add detail page url field
        Done by magic field middleware 3. if in test mode, default add address 'url' field for each item
    '''
    keywords= set(['__use','__list','__sel'])
    def parse_with_rules(self,response,rules,item_class):
        self.count = self.count+1
        logger.info("current.response.url is "+response.url+",number:"+str(self.count))
        sel = Selector(response)
        if sel is None:
            return []
        #import pdb; pdb.set_trace()
        items = []

        if issubclass(item_class,scrapy.Item):
            self.traversal(sel,rules,item_class,None,items)
        elif item_class == dict:
            self.traversal_dict(sel,rules,item_class,None,items)
        else :
            print('item_class=%s should be instance of Item or its subclass'%str(item_class))
        return items

    def extract_field(self,sels):
        contents=[]
        for i in sels:
            #remove noisy characters(unicode whitespace characters:\t\n\r\f\v)
            content=re.sub(r'\s+',' ',i.extract())
            if content !=' ':
                content = content.strip()
                contents.append(content)
        return contents
        
    def handle_text(self,selector,rules,item,k,v):
        #extract item from rules
        _sel=rules.get('__sel','css')
        if _sel =='xpath':
            _item = self.extract_field(selector.xpath(v))
        elif _sel =='css':
            _item = self.extract_field(selector.css(v))
        if '__list' in rules and False ==rules.get('__list',True):#force getting the first value
            item[k] = _item[0] if len(_item)>1 else ''
        #    if len(_item) >=1:
        #        item[k] = _item[0]
        #   else:
        #       item[k] = ''
        else:
            item[k] = _item
        
    def extract_items(self,sel,rules,single_item):
        for rk,rv in rules.items():
            if rk in self.keywords:
                continue
            if rk not in single_item:
                single_item[rk] = []
            sel_css_field=sel.css(rv)
            #sel_css_field=sel.xpath(rv)
            if sel_css_field:
                single_item[rk] += self.extract_field(sel_css_field)
            else:
                single_item[rk] =[]
            

    def traversal(self,sel,rules,item_class,item,items):
        '''
        item : single Instant
        Items:list that includes all item
        '''
        if item is None:
            item = item_class()

        if '__use' in rules:
            if '__list' in rules and True ==rules.get('__list',True):
                single_item = item_class()
                self.extract_items(sel,rules,single_item)
                items.append(single_item)
            else:#TODO: force first value
                self.extract_items(sel,rules,item)
            #import pdb; pdb.set_trace()
            #logger.info('extract_items:'+str(items))
        else:
            for rk,rv in rules.items():

                #for i in sel.xpath(rk):
                for i in sel.css(rk):
                    self.traversal(i,rv,item_class,item,items)

    def traversal_dict(self,sel,rules,item_class,item,items):
        item={}
        for k,v in rules.items():
            #if dict!= type(v):
            if isinstance(v,dict) ==False:
                if k in self.keywords:
                    continue
                # handle the item field
                self.handle_text(sel,rules,item,k,v)
            else:
                #continue traversing the nested dict
                item[k] = []
                for i in sel.css(k):
                #for i in sel.xpath(k):
                    #print(">>>>>>>>>>>>>>>>>print rule: ",k,v)
                    self.traversal_dict(i,v,item_class ,item,item[k])
        items.append(item)



    ''' # use parse_with_rules example:
    def parse_people_with_rules(self, response):
        item = self.parse_with_rules(response, self.all_css_rules, Item)
        item['id'] = urlparse(response.url).path.split('/')[-1]
        info('Parsed '+response.url) # +' to '+str(item))
        return item
    '''



