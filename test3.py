#coding=utf-8
import random
import time
from time import sleep


__author__ = 'ymq'
import urllib.request
from selenium import webdriver
import urllib
import sys
import re

import os.path
import requests
from bs4 import BeautifulSoup
from contextlib import closing

url = "http://fcw54.com/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

# driver=webdriver.Firefox(executable_path = '/usr/local/lib/python3.6/geckodriver')
driver = webdriver.Chrome(executable_path='/usr/local/lib/python3.6/chromedriver', chrome_options=chrome_options)
driver.implicitly_wait(10)

def _downloader(video_url, path):
    ip = ['121.31.159.197', '175.30.238.78', '124.202.247.110', '10.0.7.555', '126.202.247.120', '128.212.117.120']
    Header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    }

    size = 0

    if os.path.exists(path):
        Header['Range'] = 'bytes=%d-' % os.path.getsize(path)
        size = os.path.getsize(path)

    with closing(requests.get(video_url, headers=Header, stream=True, verify=False)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        if content_size == size:
            print("文件已存在")
            return

        if response.status_code == 200:
            sys.stdout.write('[File Size]: %0.2f MB\n' % (content_size/chunk_size/1024))
            with open(path, 'wb') as f:
                for data in response.iter_content(chunk_size=chunk_size):
                    f.write(data)
                    size += len(data)
                    f.flush()
                    sys.stdout.write('\r[Progress]: %0.2f%%' % float(size/content_size*100))
                    sys.stdout.flush()



def doRequest(url):
    print("开始请求")
    try:
        fuckyou_header= {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        req = urllib.request.Request(url,headers=fuckyou_header)

        content = urllib.request.urlopen(req).read()
        content = content.decode('utf-8',"ignore")
    except urllib.request.URLError as e:
        if hasattr(e,"reason"):
            print (u"连接失败,错误原因",e.reason)
            return None
    return content

def startRequest():
    content = doRequest(url)
    soup = BeautifulSoup(content,"html.parser")
    navigation = soup.find(attrs={"class":"navigation"})
    titles = navigation.findAll("a")

    selectBook = input("请输入视频类型：")
    title = titles[int(selectBook)]
    print(title.get("href"))
    print(title.string)
    content1 = doRequest(url)
    soup1 = BeautifulSoup(content1,"html.parser")
    navigation1 = soup1.find(attrs={"class":"main-content"})
    titles1 = navigation1.findAll('a')

    resArr = []

    for temp in titles1:
        temptitle = temp.get("href")
        if temptitle != "#":
            resArr.append(temptitle)





    # content3 = doRequest(aaaa)
    # print(content3)




    # info = BeautifulSoup(content3,"html.parser")
    # r = re.findall(r'<script type="text/javascript">\n([\s\S]+?)</script>', content3, re.M) #截取javascript代码
    #
    # str="video_url: 'function/0/(.*?)/',.*?"
    # pattern = re.compile(str,re.S)
    # items = re.findall(pattern, content3)
    # print(items)
    count = 0

    while( count < len(resArr)):
        aaaa = resArr[count]
        print("开始下载" + aaaa)
        driver.get(aaaa)

        str1 = u"下载:"
        str= str1 + '.*?<a href="(.*?)".*?'
        pattern = re.compile(str,re.S)
        items = re.findall(pattern, driver.page_source)
        print(items[0])

        path = "/Users/iyunshu/Desktop/aaaaaa/" + driver.title + ".mp4"
        _downloader(items[0], path)

        count += 1

    print("下载完毕")


startRequest()
