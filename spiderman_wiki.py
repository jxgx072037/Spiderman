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
random.seed(datetime.datetime.now()

#函数：获取页面wiki词条a标签的href属性
def getLinks(url):
    try:
        html = urlopen('https://en.wikipedia.org'+url)
    except HTTPError as e:
        print (e)
        return None
    try:
        bsObj = BeautifulSoup(html.read(), 'lxml')
        web_info = bsObj.find('div', {'id':'bodyContent', }).findAll('a', href = re.compile('\/wiki\/((?!:).)*$'))
    except AttributeError as e:
        print (e)
        return None
    return web_info


links = getLinks('/wiki/Kevin_Bacon')
if links == None:
    print ('Links could not be found, check the code.')
else:
    while len(links)>= 0:
        new_url = links[random.randint(0, len(links)-1)].attrs['href']
        print(new_url)
        getLinks(new_url)