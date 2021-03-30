# Stackoverflow crawler

Spider for Stackoverflow clockIn Counter

## Process
1) write scheduled script to open up stackoverflow clockIn 
2) schedule job daily by windows scheduled tool
3) after that,run the spider to retrieve counter and compare with previous counter
4) retry script if neccessary


## Change Log

1.2018-08-27:initial and add mail feature for spider


## ENV
   * [Scrapy](https://doc.scrapy.org/en/latest/intro/install.html)

## Usage

	```
	scrapy crawl SO_Badge_counter    
	```


