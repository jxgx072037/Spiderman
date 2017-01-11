from urllib.request import urlopen
from urllib.error import URLError
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import ssl
import datetime
import random

#关掉ssl的证书验证功能
ssl._create_default_https_context = ssl._create_unverified_context

#用系统当前时间做一个随机数生成器
random.seed(datetime.datetime.now())

pages = set()

#函数：获取页面wiki词条a标签的href属性
def getLinks(url):
    global pages
    try:
        html = urlopen('https://en.wikipedia.org'+url)
    except HTTPError as e:
        print (e)
        return None
    try:
        bsObj = BeautifulSoup(html.read(), 'lxml')
        web_info = bsObj.find('div', {'id':'bodyContent'}).findAll('a', href = re.compile('/wiki/((?!:).)*$'))
        for link in web_info:
            if 'href' in link.attrs:
                if link.attrs['href'] not in pages:
                    print(bsObj.find('h1').string)
                    print(bsObj.find('div', {'id': 'mw-content-text'}).find('p').get_text())
                    try:
                        print(bsObj.find('a', {'class': 'wbc-editpage'}).attrs['href'])
                    except AttributeError as e:
                        print('%s页面缺少相关属性' % url)
                    newPage = link.attrs['href']
                    # print(newPage)
                    pages.add(newPage)
                    print(pages)
                    print('\n')
                    getLinks(newPage)
    except AttributeError as e:
        print (e)
        return None
    return web_info

getLinks('')
