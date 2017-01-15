# encoding:utf-8
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
cur.execute('SHOW tables;')
table_tuple = (cur.fetchall())
#删除数据库中已经存在的表
for i in range(0, len(table_tuple)):
    drop_table = 'DROP TABLE IF EXISTS %s;' %(table_tuple[i][0])
    cur.execute(drop_table)
#创建province_info，存储省名称和省链接
sql_province = '''CREATE TABLE province_info (id BIGINT(7) NOT NULL AUTO_INCREMENT, province_name VARCHAR(20),
                province_link VARCHAR(500), created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (id));'''
cur.execute(sql_province)
#创建region_info，存储区域名称和区域链接
sql_region = '''CREATE TABLE region_info (id BIGINT(7) NOT NULL AUTO_INCREMENT, province_name VARCHAR(20),
                province_link VARCHAR(500), created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
             PRIMARY KEY (id));'''
cur.execute(sql_region)

# 关闭ssl的证书验证功能
ssl._create_default_https_context = ssl._create_unverified_context()

#在province_info中存储省和对应的省链接
def storeprovincelink(region, link):
    cur.execute("INSERT INTO province_info (province_name, province_link) VALUES ('%s', '%s');" % (region, link))
    return

def storeregionlink(region, link, n):
    cur.execute("INSERT INTO region_info (region%d_name, region%d_link) VALUES ('%s', '%s');" % (n , n ,region, link))
    return

startPage = 'http://www.byeah.net/rock/search/index/t/loc.html'

# 获取省链接
def get_provinceLink():
    try:
        html = urlopen(startPage)
    except HTTPError as e:
        print (e)
        return None
    try:
        bsObj = BeautifulSoup(html.read(), 'lxml')
        for link in bsObj.findAll('a', {'class':'list-group-item'}):
            storeprovincelink(link['title'], 'http://www.byeah.net'+link['href'])
    except AttributeError as e:
        print (e)
        return None

s = 0 #s记录子地区层数

def get_regionLink_recursion(link, n):
    global s
    try:
        html = urlopen(link)
    except HTTPError as e:
        print(e)
        return None
    try:
        bsObj = BeautifulSoup(html.read(), 'lxml')
        inferior_region = bsObj.find('h3',text='子地区')
        if None is not inferior_region:
            inferior_region= inferior_region.parent.next_sibling.next_sibling  # findAll是resultType，没有parent属性。通常next_sibling是换行，显示空白，所以还要再来一次。
            n = n + 1
            if n > s:
                cur.execute('ALTER TABLE region_info ADD region%d_name VARCHAR(20), ADD region%d_link VARCHAR(500);' % (n, n))
                s = n
            inferior_regions = inferior_region.findAll('a')
            for region in inferior_regions:
                print (region)
                storeregionlink(region['title'], 'http://www.byeah.net'+region['href'], n)
                get_regionLink_recursion('http://www.byeah.net'+region['href'], n)
        else:
            return
    except AttributeError as e:
        print(e)
        return None


try:
    get_provinceLink()
    cur.execute('SELECT province_link FROM province_info;')
    for province_link in cur.fetchall():
        print (province_link[0])
        get_regionLink_recursion(province_link[0], 0)
    cur.execute('SELECT * from region_info')
    print(cur.fetchall())

finally:
    cur.close()
    conn.close()


