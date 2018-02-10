
import scrapy



class QuotesSpider(scrapy.Spider):
    name="quotes"

    def start_requests(self):
        urls=[
            'http://quotes.toscrape.com/page/1/',
           #'http://quotes.toscrape.com/page/2/',
            ]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    # parse content from response and save into files
    def parse(self,response):
        page = response.url.split('/')[-2]
        filename = 'feeds/quotes/quotes-%s.html'%page
        with open(filename,'wb') as fn:
            fn.write(response.body)
        self.log('Saved file %s'% filename)
        
        for quote in response.css('div.quote'):
            yield {
                    'text': quote.css('span.text::text').extract_first(),
                    'author':quote.css('small.author::text').extract_first(),
                    'tags':quote.css('div.tags a.tag::text').extract(),
                }
        # pass a string
        #next_page=response.css('li.next a::attr(href)').extract_first()
        #if next_page is not None:
            
            #next_page = response.urljoin(next_page)
            #yield scrapy.Request(next_page,callback=self.parse)
            #Or
        #  yield response.follow(next_page,callback = self.parse)

        #pass a selector
        #for href in response.css('li.next a::attr(href)'):
        #      yield response.follow(href,callback=self.parse)
        #Or
        for a in response.css('li.next a'):
            yield response.follow(a,callback =self.parse)
