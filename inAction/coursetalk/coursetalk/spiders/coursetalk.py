import scrapy
import logging

class ListaDeCursosSpider(scrapy.Spider):
    name = "lista_de_cursos"
    allowed_domains = ['www.coursetalk.com']
    start_urls = ['https://www.coursetalk.com/subjects/data-science/courses/'] 

    def start_requests(self):
        urls=[
            'https://www.coursetalk.com/subjects/data-science/courses/'
        ]
        # headers={
        #     'User-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        #     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        #     'Accept-encoding':'gzip, deflate, br',
        #     'Accept-language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        # }
        for url in urls:
        	yield scrapy.Request(url = url,callback=self.parse)



    def parse(self, response):
        logging.info("response.status:%s"%response.status)
        #logging.info("response.body:%s"%response.body)
        logourl = response.selector.css('div.main-nav__logo img').xpath('@src').extract()
        logging.info('response.logourl:%s'%logourl)