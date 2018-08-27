import requests


# image download
def request(filePath, url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    r = requests.get(url, headers=headers)
    with open(filePath, 'wb') as f:
        f.write(r.content)
