from urllib import parse

# **==== val ============================
URL = 'https://goodinfo.tw/tw/StockList.asp'
ENCODING = 'utf-8'

HEADERS = {'content-type': 'application/x-www-form-urlencoded;',
           'content-length': '0',
        #    'referer': URL + parse.urlencode(PARAMS),
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.55'}


SORT_FIELDS = ['股東<br>權益<br>(億)']
