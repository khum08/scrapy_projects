# coding:utf-8
from collections import OrderedDict
import json
import hashlib
import time
import requests
import random
import string

KEY = '&%2F&EFUNONG&%2F&'
APP_ID = "TESTGSjQdeemWeRb4oLomQx4dWLV8D"
HOST = "192.168.0.142:9015"


# 生成签名
def create_sign(appid, timestamp, nance_str, data):
    dic1 = {
        'appid': appid,
        'timestamp': timestamp,
        'noncestr': nance_str
    }
    dic = dict(dic1.items() + data.items())
    dic = OrderedDict(sorted(dic.items()))
    query_string = ''
    for key, value in dic.items():
        if isinstance(value, dict):
            value = json.dumps(value).replace(" ", "")
        query_string += '&' + str(key) + "=" + str(value)
    string_to_sign = KEY + query_string[1:]
    print(string_to_sign)
    sha1 = hashlib.sha1(string_to_sign)
    return sha1.hexdigest()


# 生成请求的url
def create_url(data, appid=APP_ID):
    t = int(time.time())
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 10)).lower()
    base_url = "http://%s/send_ordinary_template_sms.json?" \
               "appid=%s&timestamp=%d&noncestr=%s&signature=" % (HOST, appid, t, nonce_str)
    sign = create_sign(appid, t, nonce_str, data)
    return base_url + sign


# 发短信
def send_sms(data):
    return requests.post(create_url(data), data=json.dumps(data))


# 测试短信借口代码
def test():
    data = {"action_id": "AiGd9MYekNz38OJG", "phone_number": "17612159408", "sms_param": {"value_01": "姓名"}}
    response = send_sms(data)
    print ("*"*30)
    print ("request_url: ", response.request.url)
    print ("request_headers: ", response.request.headers)
    print ("request_body: ", response.request.body)
    print ("*"*30)
    print (response.status_code, response.reason)
    print (response.content)

# test()

"""
发送普通模板短信：
POST请求
URL：
http://192.168.0.142:9015/send_ordinary_template_sms.json?
appid=LHYhND82WCkOKZsFfwFuiCMlrOR2RW&timestamp=xxx&noncestr=xxx&signature=xxx

JSON PARAM：
{"action_id":"A635OnxUQ41hKRfm","phone_number":"xxx","sms_param":{"value_01":"姓名"}}
"""
