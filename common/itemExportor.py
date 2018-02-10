# -*- coding: utf-8 -*-
from logging

from scrapy.exporters import BaseItemExporter,JsonItemExporter,JsonLinesItemExporter

logger = loggging.getLogger(__name__)


#add to settings.FEED_EXPORTERS section
class UnicodeJsonItemExporter(JsonItemExporter):

    def __init__(self,file,**kwrgs):
        JsonItemExporter.__init__(self,file,ensure_ascii = False,**kwrgs)


    def encode_list(self,data):
        rv = []
        for item in data:
            if isinstance(item,unicode):
                item = item.encode('utf-8')
            elif isinstance(item,dict):
                item = self.encode_dict(item)
            elif isinstance(item,list):
                item = self.encode_list(item)
            rv.append(item)
        return rv

    def encode_dict(self,data):
        rv={}
        for key,value in data.items():
            if isinstance(key,unicode):
                key = key.encode('utf-8')
            if isinstance(value,unicode):
                value = value.encode('utf-8')
            elif isinstance(value,list):
                value = self.encode_list(value)
            elif isinstance(value,dict):
                value = self.encode_dict(value)
            rv[key] = value
        return rv

    #export the given item
    def export_item(self,item):
        if self.first_item:
            self.first_item = False
        else:
            self.file.write(',\n')
        itemdict = dict(self._get_serialized_fields(item))
        itemdict = self.encode_dict(itemdict)
        self.file.write(self.encoder.encode(itemdict))