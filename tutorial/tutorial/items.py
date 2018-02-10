# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class OlxItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    user = scrapy.Field()
    url = scrapy.Field()



class DmoztoolsItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    description=scrapy.Field()

class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    last_updated = scrapy.Field(serializer =str)# what mean ?


print("dictionary started....")
product=Product(name='Desktop PC',price =1000)
print(product)
print(product['name'])
print(product['price'])
#print(product['last_updated'])
#print(product['last_updated','not set'])

#print(product.get('lala'))
print(product.get('lala','unknown field'))

print("is name field populated? ",'name' in product) 

#set field
product['last_updated']= 'today'
print(product['last_updated'])

#product['lala']='test' #not support to set unknown field name

print(product.keys())

print(product.items())

#copy dicts from items
product2= Product(product)
print(product2)
#or
product3=product2.copy()
print(product3)

product = Product(name='Desktop PC',price = 1000)

print(product)
#if dictionary key is not defined,then would raise an error
try:
    if product["test"]:
        product["test"]="test"  
except KeyError:
    print("e")
print(product)

#extending item
class DiscountedProduct(Product):
    discounted_percent = scrapy.Field(serializer=str)
    discount_expiration_date = scrapy.Field()
    name = scrapy.Field(Product.fields['name'],serializer=str)



print(DiscountedProduct.fields)


#Test dict
item_rules = {
        'div.cat-list.results.leaf-nodes .cat-item': {
            '__use': 'dump',
            '__list': True,
            'url': 'a::attr(href)',
            'name': 'a::text',
            'description': 'li::text',
        }
}
for nk,nv in item_rules.items():
    print("\n nkey:"+nk)
    if isinstance(nv,dict):
        for k,v in nv.items():
            print("\n key:"+ k )
            print("value:"+ str(v) )
    else:
        print('nvalue:'+nv)

    print('test dictionary finished...')


from urllib.parse import urlparse

url= 'http://books.toscrape.com/catalogue/soumission_998/index.html'
uri = urlparse(url).path.split('/')
print("uri = urlparse(url).path.split('/')",urlparse(url).path.split('/')[-2])
print("uri",str(uri))
for i in range(0,len(uri)):
    print(i,uri[i])


import sys
import os
from os.path import dirname
path = dirname(dirname(os.path.abspath(os.path.dirname(__file__))))
print("path",path)

