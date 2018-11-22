# coding:utf-8
import scrapy
import sys
import urllib
import requests

import SmsUtil
import json

from scrapy.selector import Selector
from ..settings import URL_USERS
from db import DbUtils

reload(sys)
sys.setdefaultencoding("utf-8")
REQUEST_OUR_SERVER_DATA = {
    "province_id": 16,
    "purpose": "畜禽养殖"
}
HEADERS = {
    'Host': '222.143.21.233:2018',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.doupotuan.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Referer': 'http://222.143.21.233:2018/pub/GongShiSearch',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': '__RequestVerificationToken_Lw__=k5+ZOxp2Pu9wyZLbQRjE4xvcVS5q+pkvA9gILSqZNnfaUBiDySOzdUr0ZbiuvBB4GG9cV9nM/AS1mO1VPwz8H5laHZ2r2YQS9J0B+XNLClFIFVxIyrMbBpXAVsyfJCeRGZOap4W0EZilOWGuZDap7Li3pMRr/jwOnvSImqFTIPQ='
}


class MySpider(scrapy.spiders.Spider):
    name = "subsidy"

    start_urls = [
        "https://www.baidu.com"
    ]

    def __init__(self):
        self.user_list = {}

    def parse(self, response):
        data = REQUEST_OUR_SERVER_DATA
        resp = requests.post(URL_USERS, data=json.dumps(data))
        a = resp.json()

        # print(json.dumps(resp.json()))
        if a['code'] == 0 and a['data']['subsidies']:
            self.user_list = a['data']['subsidies']
            # print(len(self.user_list))
            for i in range(len(self.user_list)):
                url = "http://222.143.21.233:2018/pub/gongshi"
                yield scrapy.Request(url, callback=lambda response, index=i: self.get_token(response, index)
                                     , dont_filter=True)

    # 获取token
    def get_token(self, response, index):
        token = response.xpath('//form//input[@name="__RequestVerificationToken"]/@value').extract()[0]
        # 测试xpath方法
        # self._test_(response)

        url = "http://222.143.21.233:2018/pub/GongShiSearch"
        json_data = json.loads(json.dumps(self.user_list))
        name = json_data[index]["name"]
        china_id = json_data[index]["china_id"]
        print(index)
        print(name)
        n = urllib.quote(name.decode(sys.stdin.encoding).encode('utf-8'))
        data = "__RequestVerificationToken=%s&n=%s&IdCard=%s&p=&areaName=&AreaCode=&qy=" % (token, n, china_id)
        print(data)
        self.crawl_result(url, data, china_id)

    # 模拟请求开始真正的查询
    def crawl_result(self, url, data, china_id):
        res = requests.post(url, data=data, headers=HEADERS)
        selector = Selector(res)
        content = selector.xpath('//tbody/tr[1]/td/text()').extract()
        # print(content)
        if content:
            # content不为空[],则查到了有数据
            print("-" * 60)
            china_id = china_id
            name = content[4].encode("utf-8").strip()
            status = content[14].encode("utf-8").strip()
            status = 0 if status == "公示" else 1
            print(name, status, china_id)
            # 查询数据库
            db = DbUtils()
            result = db.query_one(china_id)
            if result == -1:
                # 用户不存在，插入数据库，发送短信通知
                db.insert_user(name, china_id, status)
                # todo
                SmsUtil.send_sms({})
            elif result != status:
                # 用户存在，状态变化，更新数据库，发送短信通知
                db.update(china_id, status)
                # todo
                SmsUtil.send_sms({})
            else:
                # 用户存在，状态没有变化，不处理
                pass
            db.close_resource()
        else:
            print('-' * 30)

    # 测试xpath的方法
    def _test_(self, response):
        test_content = response.xpath('//tbody/tr[1]/td/text()').extract()
        for x in test_content:
            print(x.encode("utf-8").strip())
        if not test_content:
            name = test_content[4].encode("utf-8").strip()
            status = test_content[14].encode("utf-8").strip()
            print(name, status)
            print("*" * 60)
