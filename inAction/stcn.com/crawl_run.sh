#!/bin/bash

rm -f exports/stcn_*.json
rm -f source/stcn_*.json source/pretty_format/stcn_*.json


#debug
scrapy crawl stcn_stock --pdb -o exports/stcn_stock.json -t json
scrapy crawl stcn_stock2 --pdb -o exports/stcn_stock2.json -t json
scrapy crawl stcn_stock3 --pdb -o exports/stcn_stock3.json -t json


#prd
#scrapy crawl stcn_stock -o exports/stcn_stock.json -t json
#scrapy crawl stcn_stock2 -o exports/stcn_stock2.json -t json
#scrapy crawl stcn_stock3 -o exports/stcn_stock3.json -t json
