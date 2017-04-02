# 作者：chias
# 说明：python爬虫入门：Heru3全站图片批量爬取。
# 日期：2016-01-24
# 博客：https://www.mrorz.com

import requests,html5lib,re,socket,socks,os,time
from bs4 import BeautifulSoup

print('''H3爬虫「抓取指定网站和下载」\n
      名称：触网虫\n
      类型：爬虫类邪恶型数码精灵\n
      状态：成长期\n
      必杀技：上下其手！\n
      说明：针对一个网站伸出触手的变态数码精灵。\n
      口号：触遍所有HTML！
      ''')
print('===========简陋的分割线===========')

#抓取网页
def spider(x):
    while True:
        try:
            r = requests.get(x,headers,timeout = 20)
            html = BeautifulSoup(r.text,'html5lib')
            sc = r.status_code#响应状态码Status Code
            break
        except:
                print('*************断线重连*************')
                print('===等待2秒后自动重试！===')
                time.sleep(2)
                continue
    return html,sc
#CSS搜索
def search_css(x,tab,class_name):
    html_class = x.find_all(tab,class_ = class_name)
    return str(html_class)
#下载
def file_download(x,path):
        while True:
                try:
                        r = requests.get(x)
                        with open(path,'wb') as file:
                                file.write(r.content)
                        break
                except:
                        print('*************断线重连*************')
                        print('===等待2秒后自动重试！===')
                        time.sleep(2)
                        continue


#抓取全站文章页面链接
def all_links(x):
    spider(x)

#网址构造函数
def url_link(x):
    url = basic_target + parameter + str(x)
    return url
#设置SOCKS5代理
socks.set_default_proxy(socks.SOCKS5,"127.0.0.1",1080)
socket.socket = socks.socksocket

#设置网址有序参数（有规律变化的参数，例如页数）
page_number = 1
#设置网址无序参数（固定参数）
parameter = '?paged='

#设置基本下载路径
download_path = r"D:\spider\h3"

#目标基本网址
basic_target = "http://heru3.com/"

#设定headers
headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'  ,
            'Referer':'http://heru3.com/'
      }

#=============运行主体============

(html,sc) = spider(basic_target)
while sc == 200:
    for link in html.find_all('h2',class_='title'):#遍历html，找出含有<h2 class="title">的标签
        j = link.find('a')#找出含"a"的子标签
        url = j.get('href')#获得带有"href"的链接
        print(url)
        print(link.string)
        print('===========简陋的分割线===========')
        (html_article,sc_article) = spider(url)#爬虫得到的链接
        if sc_article == 200:
            f_path = download_path + '\\' + re.sub('[/\!#$^%&*~]','',link.string)
            if os.path.isdir(f_path):
                pass
            else:
                os.makedirs(f_path)#创建文件夹，以文章标题为名
            for download_link in html_article.find_all('dt',class_='gallery-icon'):
                f = download_link.find('a')
                down_url = f.get('href')
                print('正在下载：',down_url)
                filename = os.path.basename(down_url)#获取链接文件名
                path = f_path  + '\\' + filename#构造下载路径
                if os.path.isfile(path):
                    pass
                else:
                    file_download(down_url,path)
                print('===KO！===')
        print('===========简陋的分割线===========')
        print('===等待5秒后再继续！===')
        time.sleep(5)
    page_number += 1
    (html,sc) = spider(url_link(page_number))
print('完成！！！！')
