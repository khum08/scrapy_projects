import urllib

import scrapy
import os

from scrapy import Request
from ..items import BeautyItem


# 爬取一个校花网站的图片
class BeautySpider(scrapy.Spider):
    name = "beauty"
    start_urls = ["http://www.xiaohuar.com/hua/"]

    def parse(self, response):
        names = response.xpath('//span[@class="price"]/text()').extract()
        schools = response.xpath('//a[@class="img_album_btn"]/text()').extract()
        raw_urls = response.xpath('//div[@class="img"]/a/img/@src').extract()
        with open("/home/yuanzhenkun/tutorial/beauty.txt", "a") as f:
            f.write("%s\t%s\t%s\t%s" % ("num", "name", "school", "url"))
        for i in range(len(names)):
            item = BeautyItem()
            pname = names[i].encode("utf-8")
            pschool = schools[i].encode("utf-8")
            purl = "http://www.xiaohuar.com/" + raw_urls[i].encode("utf-8")
            print("%s\t%s\t%s\t%s" % (str(i), str(pname), str(pschool), str(purl)))
            print("-----------------------------------")
            item["index"] = i
            item['name'] = str(pname)
            item['school'] = str(pschool)
            item['url'] = purl
            yield item
            # 把记录写入文件，同时下载照片
            if purl:
                with open("/home/yuanzhenkun/tutorial/beauty.txt", "a") as f:
                    f.write("%s\t%s\t%s\t%s" % (str(i), str(pname), str(pschool), str(purl)))
                file_name = "%d_%s.jpg" % (i, pname)
                file_path = os.path.join("/home/yuanzhenkun/tutorial/pic", file_name)
                urllib.urlretrieve(purl, file_path)

        # 获取更多链接
        all_urls = response.xpath('//a/@href').extract()
        for url in all_urls:
            if url.startswith("http://www.xiaohuar.com/list-1-"):
                yield Request(url, callback=self.parse)
        print("\n\n")
