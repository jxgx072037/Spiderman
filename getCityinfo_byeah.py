# encoding:utf-8
# 以下代码用于获取byeah的所有城市，并存储在数据库climbing_guide的city_info表中.
# pymysql相关教程请见：http://www.open-open.com/lib/view/open1424699022093.html
from urllib.request import urlopen
from urllib.error import URLError
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import ssl
import re #正则表达式模块
import pymysql

conn = pymysql.connect(host='localhost', user='root', passwd='nrypx5iv', db='climbing_guide', charset='utf8') #建立和数据库climbing_guide的链接
cur = conn.cursor() #建立光标
drop = 'DROP TABLE IF EXISTS city_info'
cur.execute(drop)
sql = 'CREATE TABLE city_info (id BIGINT(7) NOT NULL AUTO_INCREMENT, city VARCHAR(20), city_link VARCHAR(1000), created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (id));'
cur.execute(sql)

ssl._create_default_https_context = ssl._create_unverified_context() #关闭ssl的证书验证功能

#在city_info中存储城市和对应的城市链接
def storeCitylink(city, link):
    cur.execute("INSERT INTO city_info (city, city_link) VALUES (%s, %s)", (city, link))
    cur.connection.commit()

startPage = 'http://www.byeah.net/rock/search/index/t/loc.html'
city_link = []

# 获取城市链接
def get_cityLink():
    try:
        html = urlopen(startPage)
    except HTTPError as e:
        print (e)
        return None
    try:
        bsObj = BeautifulSoup(html.read(), 'lxml')
        for link in bsObj.find('div', {'class':'list'}).findAll('a'):
            storeCitylink(link['title'], 'http://www.byeah.net/'+link['href'])
    except AttributeError as e:
        print (e)
        return None

try:
    get_cityLink()
    cur.execute('SELECT * FROM city_info;')
    print (cur.fetchall())

finally:
    cur.close()
    conn.close()


