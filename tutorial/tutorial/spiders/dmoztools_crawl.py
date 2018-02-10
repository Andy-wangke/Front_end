# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request

import logging
import pprint
import re

from tutorial.items import DmoztoolsItem




class DmoztoolsSpider(CrawlSpider):
    name = 'dmoztools'
    allowed_domains = ['dmoztools.net']
    start_urls = ['http://dmoztools.net/']

    count=0

    valid_categories = [
        'Arts', 'Business', 'Computers', 'Games', 'Health', 'Home',
        'Kids_and_Teens', 'News', 'Recreation', 'Reference', 'Regional', 'Science',
        'Shopping', 'Society', 'Sports',
        ]
    allow_rules= ['/{}/'.format(i)
                                  for i in valid_categories ]
    rules = (#TODO  deny url '/World//...'
        #Rule(LinkExtractor(allow='',deny='/World/.*'),callback = 'parse_item',follow = False),
        Rule(LinkExtractor(allow=allow_rules,deny='/World/.*',restrict_xpaths='//h2[@class="top-cat"]'), callback='parse_item', follow=False),
    )

    keywords= set(['__use','__list'])
    item_rules = {
        'div.cat-list.results.leaf-nodes .cat-item': {
            '__use': 'dump',
            '__list': True,
            'url': 'a::attr(href)',
            'name': 'a::text',
            'description': 'li::text',
        }
    }

    def parse_item(self, response):
        logging.info("Parsing depth 1:"+response.url+',response.depth:'+str(response.meta['depth']))
        items = []
        #DmoztoolsItem
        items = self.parse_with_rules(response,self.item_rules,dict)
        #pprint.pprint(items)
        import pdb; pdb.set_trace
        #
        
        

    '''
        Provide the common spider funtion
        item_class is initial dict , then traverse
        item_class is specified,then traverse by corresponding item
    '''
    def parse_with_rules(self,response,rules,item_class,force_one_item=False):
        self.count = self.count+1
        logging.info("this.response.url is "+response.url+",count:"+str(self.count))
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
            content=re.sub(r'\s+',' ',i.extract())#remove noisy characters
            if content !=' ':
                contents.append(content)
        return contents
        
    def handle_text(self,selector,item,force_first_item,k,v):
        #extract item from rules
        _item = self.extract_item(selector.css(v))
        if force_first_item:
            if len(_item) >=1:
                item[k] = _items[0]
            else:
                item[k] = ''
        else:
            item[k] = _item
        
        

    def traversal(self,sel,rules,item_class,item,items):
        '''
        item : single Instant
        Items:list that includes all item
        '''
        pass


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
                    print(k,v)
                    self.traversal_dict(i,v,item_class ,item,item[k],force_one_item)
                    
        items.append(item)
        
        



        
