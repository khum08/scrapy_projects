# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NongziItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 作物名字
    crop_name = scrapy.Field()
    # 图片名字
    image_name = scrapy.Field()
    # 图片URL
    image_url = scrapy.Field()
    # 图片网址
    image_site_url = scrapy.Field()
    # 图片网址标题
    image_site_title = scrapy.Field()
    # 图片号码
    num = scrapy.Field()
