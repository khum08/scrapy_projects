# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import scrapy
import os
from scrapy.pipelines.images import ImagesPipeline


class CropBasePipeline(object):

    def __init__(self):
        self.f = open("apple.json", 'a')
        self.f.write("[\n")

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.f.write(content.encode("utf-8"))
        self.f.flush()
        return item

    def close_spider(self, spider):
        self.f.write("\n]")
        self.f.close()


class ImageDownPipeline(ImagesPipeline):
    """docstring for imageDownPipeline"""

    def get_media_requests(self, item, info):
        url = item['image_url']
        yield scrapy.Request(url)

    def item_completed(self, results, item, info):
        image_path = [x["path"] for ok, x in results if ok]
        image_store = '/home/yuanzhenkun/py_project/scrapy_project/crop_base/images/apple'
        os.rename(image_store + image_path[0], image_store + item["image_name"])
        return item
