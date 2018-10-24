from bs4 import BeautifulSoup as BS
import ssl
from urllib import parse
from urllib import request
from urllib.request import Request, urlopen
import traceback
from fake_useragent import UserAgent

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response

flask_app = Flask(__name__)

@flask_app.route('/searchKeyword', methods = ['GET', 'POST'])
def search_keyword():
    if request.method != 'POST':
        return

    keyword = request.form['keyword']
    input_url = request.form['url']
    base_url = 'https://search.naver.com/search.naver'

    values = {
        'where' : 'post',
        'sm' : 'tab_jum',
        'query' : keyword
    }

    query_string = parse.urlencode(values, encoding='UTF-8', doseq=True)
    context = ssl._create_unverified_context()
    rank = '순위 밖'
    url = ''
    try:
        ua = UserAgent()
        req = Request(base_url + '?' + query_string, headers={'User-Agent': str(ua.chrome)})
        res = urlopen(req)
        html_data = BS(res.read(), 'html.parser')

        g_list = html_data.find_all('dd', attrs={'class' : 'txt_block'})
        try:
            urls = []
            for g in g_list:
                url = g.find('a', attrs={'class' : 'url'})
                if url:
                    url_name = url.get_text()
                    urls.append(url_name)

            for i in range(0, 5):
                if urls[i] == input_url:
                    rank = '%s위' %(i + 1)
        except:
            traceback.print_exc()
    except:
        traceback.print_exc()
    
    return render_template('index.html', url=input_url, keyword=keyword, rank=rank)


@flask_app.route('/')
def index():
    return render_template('index.html', url=" ", keyword=" ", rank=" ")


if __name__ == '__main__':
    flask_app.run()
