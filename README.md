# Novel_spider_use_requests
用requests库爬取笔趣阁小说

笔趣阁小说网址
https://www.52bqg.com/

版本v1.0
1. 单线程，正则解析
2. 输入第一章节的网址
3. 生成小说的txt文件

爬取逻辑
1. 请求第一章的网页
2. 返回数据中解析的上一章url和下一章url，这里的上一章url即是目录页url
3. 把数据中的小说部分解析写入txt，继续请求下一章url
4. 解析下一章url小说部分写入txt，继续请求下下章url
5. 直到下一章url是目录页url时，说明已经爬到了最后一章，解析完后可以结束爬虫
