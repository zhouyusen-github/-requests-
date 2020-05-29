import requests
import time
from lxml import etree


def chapter_url_list(catalogue_html_tree):
    url_list = catalogue_html_tree.xpath("//*[@id='list']/dl/dd/a/@href")
    return url_list


def chapter_title_list(catalogue_html_tree):
    title_list = catalogue_html_tree.xpath("//*[@id='list']/dl/dd/a/text()")
    return title_list


def chapter_string(chapter_html_tree):  # 从html中解析出小说文字
    result = chapter_html_tree.xpath("// *[ @ id = 'content'] / text()")
    chapter_string = "\n".join(result).replace("\n\r", "").replace("\n\n", "\n")  # 拼接，然后消去无用回车
    return chapter_string


def request_url_html_tree(url):  # 输入url返回可用于xpath解析的对象
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response_html = response.content.decode('GB18030', 'ignore')  # 将网页的gbk编码转换为unicode
    return etree.HTML(response_html)


def write_chapter(novel, title, chapter_html_tree):  # 负责将html代码中读取的一个章节写入文件
    print(title)
    novel.write(title)
    novel.write(chapter_string(chapter_html_tree))
    novel.write("\n\n\n")


# 逻辑部分
catalogue_url = input("请输入小说目录页的网址(python输入后光标移到冒号前):")  # https://www.52bqg.com/book_361/
print("开始爬取")
time_begin = time.time()
novel = open('爬取小说.txt', 'w', encoding='utf-8')  # 创建txt文件保存小说
catalogue_url_html_tree = request_url_html_tree(catalogue_url)
url_list = chapter_url_list(catalogue_url_html_tree)
title_list = chapter_title_list(catalogue_url_html_tree)
for url, title in zip(url_list, title_list):
    complete_chapter_url = "{catalogue_url}/{url}".format(catalogue_url=catalogue_url, url=url)
    chapter_html_tree = request_url_html_tree(complete_chapter_url)
    write_chapter(novel, title, chapter_html_tree)
novel.close()
time_end = time.time()
time = round(time_end - time_begin)
print("正常结束,耗时:", time, "s")
