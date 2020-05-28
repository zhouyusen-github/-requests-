import requests

url = "https://www.52bqg.com/book_361/246328.html"

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

response = requests.request("GET", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
