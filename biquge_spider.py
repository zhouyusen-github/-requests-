import requests
import time
from lxml import etree
import threading


def chapter_url_list(catalogue_html_tree):
    url_list = catalogue_html_tree.xpath("//*[@id='list']/dl/dd/a/@href")
    return url_list


def chapter_title_list(catalogue_html_tree):
    title_list = catalogue_html_tree.xpath("//*[@id='list']/dl/dd/a/text()")
    return title_list


def chapter_string(chapter_html_tree):  # 从html中解析出小说文字
    result = chapter_html_tree.xpath("// *[ @ id = 'content'] / text()")[1:]  # 删除广告文字
    chapter_string = "".join(result).replace("\n\r", "")  # 拼接，然后消去无用回车
    return chapter_string


def request_url_html_tree(url):  # 输入url返回可用于xpath解析的对象
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response_html = response.content.decode('GB18030', 'ignore')  # 将网页的gbk编码转换为unicode
    return etree.HTML(response_html)


def storage_chapter(chapter_list, order_number, title, chapter_html_tree):  # 负责将html代码中读取的一个章节写入文件
    chapter_list[order_number][0] = title
    print(title)
    chapter_list[order_number][1] = chapter_string(chapter_html_tree)


# 逻辑部分
# catalogue_url = input("请输入小说目录页的网址(python输入后光标移到冒号前):")  # https://www.52bqg.com/book_361/
catalogue_url = "https://www.52bqg.com/book_361/"
print("开始爬取")
time_begin = time.time()

catalogue_url_html_tree = request_url_html_tree(catalogue_url)
url_list = chapter_url_list(catalogue_url_html_tree)
title_list = chapter_title_list(catalogue_url_html_tree)
order_number = 0
chapter_list = [["0" for col in range(2)] for row in range(len(url_list))]
for url, title in zip(url_list, title_list):
    complete_chapter_url = "{catalogue_url}/{url}".format(catalogue_url=catalogue_url, url=url)
    chapter_html_tree = request_url_html_tree(complete_chapter_url)
    storage_chapter(chapter_list, order_number, title, chapter_html_tree)
novel = open('爬取小说.txt', 'w', encoding='utf-8')  # 创建txt文件保存小说
for i in chapter_list:
    print("写入："+i[0])
    novel.write(i[0])
    novel.write(i[1])
    novel.write("\n\n\n")
novel.close()
time_end = time.time()
time = round(time_end - time_begin)
print("正常结束,耗时:", time, "s")
