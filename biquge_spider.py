import requests
import time
from lxml import etree
from concurrent.futures import ThreadPoolExecutor


def novel_name(catalogue_html_tree):
    name = catalogue_html_tree.xpath("//*[@id='info']/h1/text()")
    return name[0]


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


def request_chapter(title, url):  # 多线程要调用的方法，输入title，url，返回章节内容字符串
    answer = '\n\n\n' + title + '\n' + chapter_string(request_url_html_tree(url))
    return answer


# 逻辑部分
catalogue_url = input("请输入小说目录页的网址(pycharm输入后光标移到冒号前再回车):")  # https://www.52bqg.com/book_361/
max_workers = int(input("请输入爬取线程数(默认20):") or 20)
print("开始爬取")
time_begin = time.time()

catalogue_url_html_tree = request_url_html_tree(catalogue_url)
url_list = chapter_url_list(catalogue_url_html_tree)
title_list = chapter_title_list(catalogue_url_html_tree)
novel_name = novel_name(catalogue_url_html_tree)
print('小说名', novel_name)
# 多线程部分
pool = ThreadPoolExecutor(max_workers=max_workers)  # 新建线程库
future_list = []
for url, title in zip(url_list, title_list):
    complete_chapter_url = "{catalogue_url}/{url}".format(catalogue_url=catalogue_url, url=url)
    future = pool.submit(request_chapter, title, complete_chapter_url)  # 线程库导入任务
    future_list.append(future)
novel = open((novel_name + '.txt'), 'w', encoding='utf-8')  # 创建txt文件保存小说
i = 1
for future in future_list:
    print("写入第{}章".format(str(i)))
    i = i + 1
    novel.write(future.result())  # future.result()是一个阻塞方法，所以不用担心写入章节的顺序改变
novel.close()
# 多线程结束
time_end = time.time()
time = round(time_end - time_begin)
print("正常结束,耗时:", time, "s")
