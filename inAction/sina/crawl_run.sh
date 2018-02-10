#!/bin/bash

#debug
scrapy crawl sina_financeV2 --pdb -o exports/sina_financeV2.json


#prd
scrapy crawl sina_financeV2 -o exports/sina_financeV2.json