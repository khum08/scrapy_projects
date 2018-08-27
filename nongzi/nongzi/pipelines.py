# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

from .spiders import ImageLoader
from .spiders.BbsSpider import SAVE_DIR


class NongziPipeline(object):
    def process_item(self, item, spider):
        print(item)
        file_path = os.path.join(SAVE_DIR, item['image_name'])
        ImageLoader.request(file_path, item['image_url'])
        return item
