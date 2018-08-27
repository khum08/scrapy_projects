# coding:utf-8
import scrapy
import RandomUtil

from ..items import NongziItem

# 特别注意梨的页面没有下一页
NAMES = ["strawberry", "watermelon", "peach", "grape", "pear", "muskmelon"]
START_URLS = [
    "http://www.191.cn/searcher.php?"
    "type=thread&step=2&keyword=%B2%DD%DD%AE&username=&threadrange=1&threadrange=1&starttime=&endtime=&fid=63",
    "http://www.191.cn/searcher.php?"
    "type=thread&step=2&keyword=%CE%F7%B9%CF&username=&threadrange=1&threadrange=1&starttime=&endtime=&fid=63",
    "http://www.191.cn/searcher.php?"
    "type=thread&step=2&keyword=%CC%D2&username=&threadrange=1&threadrange=1&starttime=&endtime=&fid=63",
    "http://www.191.cn/searcher.php?"
    "type=thread&step=2&keyword=%C6%CF%CC%D1&username=&threadrange=1&threadrange=1&starttime=&endtime=&fid=63",
    "http://www.191.cn/searcher.php?"
    "type=thread&step=2&keyword=%C0%E6&username=&threadrange=1&threadrange=1&starttime=&endtime=&fid=63",
    "http://www.191.cn/searcher.php?"
    "type=thread&step=2&keyword=%CC%F0%B9%CF&username=&threadrange=1&threadrange=1&starttime=&endtime=&fid=63"
]
CHINESE_NAMES = ['草莓', '西瓜', '桃', '葡萄', '梨', '甜瓜']
INDEX = 1
SAVE_DIR = "/home/yuanzhenkun/py_practice/scrapy_project/ScrapyProject/nongzi/images/" + NAMES[INDEX]


class BbsSpider(scrapy.spiders.Spider):
    name = NAMES[INDEX]

    start_urls = [
        START_URLS[INDEX]
    ]

    def __init__(self):
        self.i = 0

    def parse(self, response):
        print("=============== start ===================")
        urls = response.xpath('//dl[re:test(@id,"search_*")]//a/@href').extract()
        for url in urls:
            self.i += 1
            print(self.i)
            print("-" * 20)
            print("http://www.191.cn/" + url)
            yield scrapy.Request("http://www.191.cn/" + url, callback=self.parse_data)
        next_page = response.xpath('//a[@class="pages_next"]/@href').extract()
        if next_page:
            yield scrapy.Request("http://www.191.cn/" + next_page[0], callback=self.parse)

    def parse_data(self, response):
        current_url = response.url
        all_images = response.xpath('//div[re:test(@class,"read*")]//td[@class="floot_right"]//img/@src').extract()
        site_title = response.xpath('//div[@class="readTop"]//h1/text()').extract()
        if site_title:
            image_site_title = site_title[0]
        else:
            image_site_title = ''
        if all_images:
            for image_url in all_images:
                if image_url.startswith("http") and not image_url.endswith(".gif"):
                    self.i += 1
                    print('*' * 40)
                    print(self.i)
                    print(image_url)
                    print(current_url)
                    item = NongziItem()
                    item['crop_name'] = CHINESE_NAMES[INDEX]
                    item['image_name'] = "%d_%s.jpg" % (self.i, RandomUtil.randomUuid())
                    item['image_site_title'] = image_site_title
                    item['image_url'] = image_url
                    item['image_site_url'] = current_url
                    item['num'] = self.i
                    yield item
