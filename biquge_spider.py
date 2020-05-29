import requests
import re
import time


def chapter_string(response_html):  # 从html中解析出小说文字
    result = re.findall('&nbsp;&nbsp;&nbsp;&nbsp;(.*?)<br />', response_html, re.S)  # 识别
    chapter_string = "\n".join(result)  # 拼接
    return chapter_string


def next_chapter_url(response_html):  # 获取下一章的url
    result = re.findall('章节目录</a> <a href="(.*?)">下一章</a>', response_html, re.S)
    return result[0]


def front_chapter_url(response_html):  # 获取上一章的url
    result = re.findall('<a href="(.*?)">上一章</a>', response_html)
    return result[0]


def get_title(response_html):  # 获取上一章的url
    result = re.findall('<h1>(.*?)</h1>', response_html)
    return result[0]


def request_url(url):
    payload = {}
    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://www.52bqg.com/book_361/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': 'fikker-I94e-tqbN=0AXYHsJQ23naNcZJNNFOpgR7HYtUOglo; fikker-I94e-tqbN=0AXYHsJQ23naNcZJNNFOpgR7HYtUOglo; Hm_lvt_cec763d47d2d30d431932e526b7f1218=1590658692; jieqiVisitTime=jieqiArticlesearchTime%3D1590658737; __gads=ID=d6e4ed37fec03f56:T=1590658760:S=ALNI_MaCwuEsGvO6rCoSPvXD4WoutOLnDA; jieqiVisitId=article_articleviews%3D361; Hm_lpvt_cec763d47d2d30d431932e526b7f1218=1590658755',
        'If-None-Match': '1590658766|'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    response_html = response.content.decode('GB18030', 'ignore')  # 将网页的gbk编码转换为unicode
    return response_html


def write_chapter(novel, response_html):  # 负责将html代码中读取的一个章节写入文件
    title = get_title(response_html)
    print(title)
    novel.write(title + "\n")
    novel.write(chapter_string(response_html))
    novel.write("\n\n\n")


# 逻辑部分
start_url = input("请输入小说第一章节的网址（输入后光标移到冒号前）：")
print("开始爬取")
time_begin = time.time()
novel = open('爬取小说.txt', 'w', encoding='utf-8')  # 创建txt文件保存小说
response_html = request_url(start_url)
write_chapter(novel, response_html)
next_url = next_chapter_url(response_html)
catalogue_url = front_chapter_url(response_html)  # 第一章的上一章按钮返回的目录页url

while next_url != catalogue_url:  # 最后一章的下一章按钮返回的是目录页url，所以某一章返回的若不是目录页url，则不是最后一章，则继续重复翻页读取章节操作
    response_html = request_url(next_url)
    write_chapter(novel, response_html)
    next_url = next_chapter_url(response_html)

novel.close()
time_end = time.time()
time = round(time_end - time_begin)
print("正常结束,耗时:", time, "s")
