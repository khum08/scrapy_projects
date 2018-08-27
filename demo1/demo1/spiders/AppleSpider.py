import scrapy
import os
import urllib
import RandomUtil
import ImageLoader
import time


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

        print(first_name)
        print(RandomUtil.randomUuid())
        print('================= 2================================')
        print(second_name)
        print(RandomUtil.randomUuid())

        print('================ len ==============================')
        print(len(first_name), len(second_name))
        print('================dict===============================')
        for d in dict(zip(first_name, second_name)).items():
            print(d)

        with open("/home/yuanzhenkun/py_project/scrapy_project/demo1/apple.txt", 'a') as f:
            f.write("%s;%s;%s\n" % ("num", "name1", "name2"))

        image_divs = response.xpath('//div[re:test(@id,"links-[A-Za-z]+-*")]')
        for i in range(len(first_name)):
            urls = image_divs.xpath('.//img[@class="img-rounded"]/@src').extract()
            with open("/home/yuanzhenkun/py_project/scrapy_project/demo1/apple.txt", 'a') as f:
                f.write("%s;%s;%s\n" % (str(i), first_name[i], second_name[i]))

        # image parse
        # image_divs = response.xpath('//div[re:test(@id,"links-[A-Za-z]+-*")]')
        # for index,div in enumerate(image_divs):
        # 	urls = div.xpath('.//img[@class="img-rounded"]/@src').extract()
        # 	print(first_name[index],urls)
        # 	for i in range(len(urls)):
        # 		if urls[i]:
        # 			print(urls[i])
        # 			fileName = "%s_%s.jpg"%(first_name[index].replace(" ","-"),RandomUtil.randomUuid())
        # 			filePath = os.path.join("/home/yuanzhenkun/py_project/scrapy_project/demo1/apple",fileName)
        # 			time.sleep(5)
        # 			ImageLoader.request(filePath,urls[i])
