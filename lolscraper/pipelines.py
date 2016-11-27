# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class MyImagesPipeline(ImagesPipeline):


    #Name download version
    def file_path(self, request, response=None, info=None):
        #item=request.meta['item'] # Like this you can use all from item, not just url.
        #        image_guid = request.url.split('/')[-1].split(':')[-1]
        image_guid = request.meta['fname'][0]
        return 'full/%s' % (image_guid)

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['image_urls'][0], meta=item)
