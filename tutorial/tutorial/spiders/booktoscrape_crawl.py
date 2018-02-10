 # -*- coding: utf-8 -*-
import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from tutorial.items  import OlxItem
from scrapy.selector import Selector
import logging
import re
import pprint

from urllib.parse import urlparse

from common.common_spider import CommonSpider

#forked from https://github.com/stummjr/books_crawler/
class BookToscrapeSpider(CommonSpider):
    name = 'booktoscrape2'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    #count = 0
    #firstly scrape the first page
    #goto next page and scraping
    def parse(self, response):
        for book_url in response.css('article.product_pod >h3 > a ::attr(href)').extract():
            yield Request(response.urljoin(book_url),callback=self.parse_book_page)
        #go to next page
        next_page=response.css('li.next > a ::attr(href)').extract_first()
        if next_page:
            if self.count <4:
                self.count = self.count+1
                yield Request(response.urljoin(next_page),callback = self.parse)


    def __init__(self,*args, **kw):
        super(BookToscrapeSpider,self).__init__(*args, **kw)
        
    #Note : if dict is a Item,then need to correspond below key with item fields
    item_xpath_rules={
        '//div[contains(@class,"product_main")]':{
                '__use':'dump',
                '__list':True,
                'title':'.//h1/text()',
                #Note : category is not under .product_main
                'category':'//ul[contains(@class,"breadcrumb")]/li[contains(@class,"active")]/preceding-sibling::li[1]/a/text()',
                'price':'.//p[contains(@class,"price_color")]/text()',
                'availability':'.//p[contains(@class,"availability")]/text()'
                #'description':''
            }
        }

    def parse_book_page(self,response):

        rule_item = self.parse_with_rules(response,self.item_xpath_rules,dict)

        if rule_item:
            try:
                rule_item.append({'id':urlparse(response.url).path.split('/')[-2]})
            except KeyError:
                print("not exist this key in item")
            logging.info("page rule_item is :"+str(rule_item))
            pprint.pprint(rule_item)
            return rule_item

    """            
    count = 0
    '''        
    #__use:[dump]
            if variable __use not exists, then loop nest,otherwise start parse
    #__list:boolean
                if variable __list exists or True,which means item field return a list,otherwise return the first value of array (array[0])
    #__sel:[css,xpath]
                if variable use css selector,then will parse rule by css,as applied to xpath


        Provide the common spider funtion
        item_class is initial dict , then traverse
        and item_class is specified,then traverse through corresponding item

        TODO:
        1. add xpath rule template Done
        2. add detail page url field
    '''
    keywords= set(['__use','__list','__sel'])
    def parse_with_rules(self,response,rules,item_class):
        self.count = self.count+1
        logging.info("this.response.url is "+response.url+",number:"+str(self.count))
        sel = Selector(response)
        if sel is None:
            return []

        items = []
        if item_class !=dict:
            self.traversal(sel,rules,item_class,None,items)
        else:
            self.traversal_dict(sel,rules,item_class,None,items)
            
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
        _item = self.extract_field(selector.xpath(v))
        if '__list' in rules and False ==rules.get('__list',True):#force the first value
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
            sel_css_field=sel.xpath(rv)
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
            if '__list' in rules or True ==rules.get('__list',True):
                single_item = item_class()
                self.extract_items(sel,rules,single_item)
                items.append(single_item)
            else:#TODO: force first value
                self.extract_items(sel,rules,item)
        else:
            for rk,rv in rules.items():
                for i in sel.xpath(rk):
                    self.traversal(i,rv,item_class,item,items)

    def traversal_dict(self,sel,rules,item_class,item,items):
        item={}
        for k,v in rules.items():
            #if dict!= type(v):#change to isinstance()
            if isinstance(v,dict) ==False:
                if k in self.keywords:
                    continue
                # handle the item field
                self.handle_text(sel,rules,item,k,v)
            else:
                #continue traversing the nested dict
                item[k] = []
                for i in sel.xpath(k):
                    #print(">>>>>>>>>>>>>>>>>print rule: ",k,v)
                    self.traversal_dict(i,v,item_class ,item,item[k])
        #logging.info("current url is :"+response.url)
        #item['url']='url'# add url item to track logging            
        items.append(item)
    """
        
