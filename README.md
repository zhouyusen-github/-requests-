# Novel_spider_use_requests
用requests库爬取笔趣阁小说

笔趣阁小说网址
https://www.52bqg.com/

版本v2.0
1. 多线程 xpath解析
2. 输入目录页的网址
3. 生成小说的txt文件

爬取逻辑

1. 请求目录页的url
2. 返回数据中解析出所有章节的url
3. 分别访问每个url，解析出小说，写入txt