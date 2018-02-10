# -*- coding: utf-8 -*-
# ref  https://medium.com/python-pandemonium/develop-your-first-web-crawler-in-python-scrapy-6b2ee4baf954
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from tutorial.items  import OlxItem
from scrapy.selector import Selector
import logging
import re
import pprint

class Olx2Spider(CrawlSpider):

    name = 'olx2'
    allowed_domains=['www.olx.com.pk']

    start_urls = [
        'https://www.olx.com.pk/computers-accessories/',
        #'https://www.olx.com.pk/tv-video-audio/',
        #'https://www.olx.com.pk/games-entertainment/'
                  ]

    rules = (
        Rule(LinkExtractor(allow='computers-accessories/\?.*?', restrict_css=('.pageNextPrev',)),callback='parse_item', follow=False),
    )

    item_css_rules={
        'div#offer_active ':{
            '__use':'dump',
            '__list':True,
            'title':'h1::text',
            'price':'div.pricelabel > strong::text',
            'user':'div.userdatabox .userdetails>span:first-child::text'
            }
        }

    item_xpath_rules={
        '//div[@id="offer_active"] ':{
            '__use':'dump',
            '__list':True,
            'title':'.//h1/text()',
            'price':'.//div[contains(@class,"pricelabel")]/strong/text()',
            'user':'.//div[contains(@class,"userdatabox")]//p[contains(@class,"userdetails")]/span[1]/text()'
            }
        }
    
    def parse_item(self,response):
        print('Processing:'+response.url)

        item_links = response.css('.large > .detailsLink::attr(href)').extract()

        for link in item_links:
            yield Request(link,callback = self.parse_detail_page)


    def parse_detail_page(self,response):
        
        #rule_items = self.parse_with_rules(response,self.item_css_rules,dict,True)
        #traverse by item
        rule_items = self.parse_with_rules(response,self.item_css_rules,OlxItem,True)
        logging.info(">>>>>>>>>>>>>>>>>> parse_with_rules hitting counts:"+str(self.count))
        if len(rule_items) > 0 :
            pprint.pprint(rule_items)
            return rule_items

    '''
        Provide the common spider funtion
        item_class is initial dict , then traverse
        item_class is specified,then traverse by corresponding item

        TODO:
        1. add xpath rule template
        2.
    '''
    count = 0
    '''        
    #__use:[dump]
            if variable __use not exists, then loop nest,otherwise start parse
    #__list:boolean
                if variable __list exists,which means items is a list,otherwise is a single Field(which means only get an Field)
    #__sel:[css,xpath]
                if variable use css selector,then will parse rule by css,as applied to xpath
    '''
    keywords= set(['__use','__list','__sel'])
    def parse_with_rules(self,response,rules,item_class,force_one_item=False):
        self.count = self.count+1
        logging.info("this.response.url is "+response.url+",number:"+str(self.count))
        sel = Selector(response)
        if sel is None:
            return []

        items = []
        if item_class !=dict:
            self.traversal(sel,rules,item_class,None,items)
        else:
            self.traversal_dict(sel,rules,item_class,None,items,force_one_item)
        
        return items

    def extract_item(self,sels):
        contents=[]
        for i in sels:
            #remove noisy characters(unicode whitespace characters:\t\n\r\f\v)
            content=re.sub(r'\s+',' ',i.extract())
            if content !=' ':
                content = content.strip()
                contents.append(content)
        return contents
        
    def handle_text(self,selector,item,force_first_item,k,v):
        #extract item from rules
        _item = self.extract_item(selector.css(v))
        if force_first_item:
            if len(_item) >=1:
                item[k] = _item[0]
            else:
                item[k] = ''
        else:
            item[k] = _item
        
    def extract_items(self,sel,rules,single_item):
        for rk,rv in rules.items():
            if rk in self.keywords:
                continue
            if rk not in single_item:
                single_item[rk] = []
            sel_css_field=sel.css(rv)
            if sel_css_field:
                single_item[rk] += self.extract_item(sel_css_field)
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
            else:#
                self.extract_items(sel,rules,item)
        else:
            for rk,rv in rules.items():
                for i in sel.css(rk):
                    self.traversal(i,rv,item_class,item,items)

    def traversal_dict(self,sel,rules,item_class,item,items,force_one_item):
        item={}
        for k,v in rules.items():
            #if dict!= type(v):#change to isinstance()
            if isinstance(v,dict) ==False:
                if k in self.keywords:
                    continue
                
                #then handle the text
                self.handle_text(sel,item,force_one_item,k,v)
            else:
                #continue traversing the nested dict
                item[k] = []
                for i in sel.css(k):
                    print(">>>>>>>>>>>>>>>>>print rule: ",k,v)
                    self.traversal_dict(i,v,item_class ,item,item[k],force_one_item)
                    
        items.append(item)
        
        
