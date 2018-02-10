# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import Selector

import logging
import pprint
import re


#ref https://github.com/geekan/google-scholar-crawler/
class googlescholarSpider(CrawlSpider):
    name = 'googlescholar'
    allowed_domains = ['google.com']
    start_urls = [
                  "http://scholar.google.com/scholar?as_ylo=2011&q=machine+learning&hl=en&as_sdt=0,5",
                #"http://scholar.google.com/scholar?q=estimate+ctr&btnG=&hl=en&as_sdt=0%2C5&as_ylo=2011",
                #"http://scholar.google.com",
        ]

    def __init__(self,start_url='',*args,**kwargs):
        if start_url:
            self.start_urls = [start_url]
        super(googlescholarSpider,self).__init__(*args,**kwargs)

    def start_requests(self):
        headers={
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-encoding':'gzip, deflate, br',
                'Accept-language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'User-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                #'X-chrome-uma-enabled':'1',

                'X-client-data':'CIe2yQEIo7bJAQjBtskBCPqcygEIqZ3KAQioo8oB',
               # 'referer':'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&as_ylo=2011&q=machine+learning&btnG='
            }
        for url in self.start_urls:
            yield Request(url,headers=headers,dont_filter = True)

    rules = (
        Rule(LinkExtractor(allow='scholar\?.*'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow='.*\.pdf')),
    )

    list_css_rules={
            '.gs_r': {
            'title': '.gs_rt a *::text',
            'url': '.gs_rt a::attr(href)',
            'related-text': '.gs_or_ggsm::text',
            'related-type': '.gs_ggsS .gs_ctg2::text',
            'related-url': '.gs_ggs a::attr(href)',
            'citation-text': '.gs_fl > a:nth-child(1)::text',
            'citation-url': '.gs_fl > a:nth-child(1)::attr(href)',
            'authors': '.gs_a a::text',
            'description': '.gs_rs *::text',
            'journal-year-src': '.gs_a::text',
            }
        }

    list_xpath_rules={
            '.gs_r': {
                'title': '.gs_rt a *::text',
                'url': '.gs_rt a::attr(href)',
                'related-text': '.gs_or_ggsm::text',
                'related-type': '.gs_ggsS .gs_ctg2::text',
                'related-url': '.gs_ggs a::attr(href)',
                'citation-text': '.gs_fl > a:nth-child(1)::text',
                'citation-url': '.gs_fl > a:nth-child(1)::attr(href)',
                'authors': '.gs_a a::text',
                'description': '.gs_rs *::text',
                'journal-year-src': '.gs_a::text',
            }
        }

    def parse_item(self, response):
        logging.info('Parsing url:'+response.url)
        import pdb; pdb.set_trace()
        #pprint.pprint(response.body)
        
        detailed_info=self.parse_with_rules(response,self.list_css_rules,dict)
        logging.info("detailed_info:"+detailed_info)
        import pdb; pdb.set_trace()
        items=[]
        if len(detailed_info) > 0 :
            items = detailed_info[0]['.gs_r']

            pprint.pprint(items)
            
        import pdb; pdb.set_trace()

        for item in items:
            if item['related-url'] == '' or item['related-type'] !='[PDF]':
                continue
            url= item['related-url']
            logging.info('pdf-url:'+ url)
            yield Request(url,callback = self.save_pdf)
            
    def save_pdf(self,response):
        path=self.get_path(response.url)
        logging.info("save file to path:"+path)
        with open(path,'wb') as f:
            f.write(response.body)


    def get_path(self,url):
        pass

    '''
        Provide the common spider funtion
        item_class is initial dict , then traverse
        item_class is specified,then traverse by corresponding item
    '''
    def parse_with_rules(self,response,rules,item_class,force_one_item=False):
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
        _item = self,extract_item(selector.css(v))
        if force_first_item:
            if len(_item) >=1:
                item[k] = _items[0]
            else:
                item[k] = ''
        else:
            item[k] = _item
        
        

    def traversal(self,sel,rules,item_class,item,items):
        pass

    keywords= set(['_use','__list'])
    def traversal_dict(self,sel,rules,item_class,item,items,force_one_item):
        item={}
        for k,v in rules.items():
            if dict!= type(v):
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
            
        

        
        





    
