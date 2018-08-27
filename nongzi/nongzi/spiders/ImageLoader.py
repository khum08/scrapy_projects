import requests
import random


# image download
def request(file_path, url):
    headers = {
        'User-Agent': "Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50"}
    r = requests.get(url, headers=headers)
    with open(file_path, 'wb') as f:
        f.write(r.content)
