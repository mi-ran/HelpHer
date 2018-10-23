from bs4 import BeautifulSoup as BS
import ssl
from urllib import parse
from urllib import request
from urllib.request import Request, urlopen
import traceback
from fake_useragent import UserAgent

keyword = input()
base_url = 'https://search.naver.com/search.naver'

values = {
    'where' : 'post',
    'sm' : 'tab_jum',
    'query' : keyword
}

query_string = parse.urlencode(values, encoding='UTF-8', doseq=True)
context = ssl._create_unverified_context()
blogs = []
try:
    ua = UserAgent()
    req = Request(base_url + '?' + query_string, headers={'User-Agent': str(ua.chrome)})
    res = request.urlopen(req)
    html_data = BS(res.read(), 'html.parser')

    g_list = html_data.find_all('dd', attrs={'class' : 'txt_block'})
    try:
        for g in g_list:
            blog = g.find('a', attrs={'class' : 'txt84'})
            if blog:
                name = blog.get_text()
                blogs.append(name)
    except:
        traceback.print_exc()
except:
    traceback.print_exc()

for b in blogs:
    print(b)
