import scrapy
import os
import urllib
import RandomUtil
import ImageLoader
import time
from ..items import CropBaseItem


class AppleSpider(scrapy.spiders.Spider):
    name = "apple"
    start_urls = [
        "https://plantvillage.psu.edu/topics/apple/infos"
    ]

    def parse(self, response):
        print("=============== start ===================")
        first_name = []
        h4 = response.xpath('//h4/text()').extract()
        for n in h4:
            name = n.encode("utf-8").strip()
            if not (name.startswith('Category') or name.strip == ""):
                first_name.append(name)
        second_name = []

        spans = response.xpath('//span[@style="font-weight:400;font-size:80%;"]')
        for span in spans:
            itext = span.xpath(".//i/text()").extract()
            temp = ''
            for s in itext:
                if s:
                    temp = temp + s.encode("utf-8") + ","
            second_name.append(temp.rstrip(','))

        for x in first_name:
            if x == '':
                first_name.remove(x)
        second_name = [s.replace('\n', '') for s in second_name]

        num = 0
        # image parse
        image_divs = response.xpath('//div[re:test(@id,"links-[A-Za-z]+-*")]')
        for index, div in enumerate(image_divs):
            urls = div.xpath('.//img[@class="img-rounded"]/@src').extract()
            print(first_name[index], urls)
            for i in range(len(urls)):
                if urls[i]:
                    item = CropBaseItem()
                    num += 1
                    uuid = RandomUtil.randomUuid()

                    file_name = "%s_%s.jpg" % (first_name[index].replace(" ", "-"), uuid)
                    file_path = os.path.join("/home/yuanzhenkun/py_project/scrapy_project/crop_base/images/apple",
                                            file_name)
                    # time.sleep(15)
                    # ImageLoader.request(file_path,urls[i])

                    item["num"] = num
                    item["disease"] = first_name[index]
                    item["cause"] = second_name[index]
                    item["image_name"] = file_name
                    item["image_url"] = urls[i]

                    yield item
        # image parse
        # image_divs = response.xpath('//div[re:test(@id,"links-[A-Za-z]+-*")]')
        # for index,div in enumerate(image_divs):
        # 	urls = div.xpath('.//img[@class="img-rounded"]/@src').extract()
        # 	print(first_name[index],urls)
        # 	for i in range(len(urls)):
        # 		if urls[i]:
        # 			print(urls[i])
        # 			file_name = "%s_%s.jpg"%(first_name[index].replace(" ","-"),RandomUtil.randomUuid())
        # 			file_path = os.path.join("/home/yuanzhenkun/py_project/scrapy_project/crop_base/images/apple",file_name)
        # 			time.sleep(5)
        # 			ImageLoader.request(file_path,urls[i])
