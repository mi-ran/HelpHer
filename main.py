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


def getPostDate(url):
    url = 'https://m.' + url 
    date = ""
    try:
        ua = UserAgent()
        req = Request(url, headers={'User-Agent': str(ua.chrome)})
        res = urlopen(req)
        html_data = BS(res.read(), 'html.parser')

        g = html_data.find('p', attrs={'class' : 'se_date'})
        try:
            date = g.get_text()
        except:
            traceback.print_exc()
    except:
        return ""
        
    return date


def search(keyword, input_url):
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
    time_ = ' '
    try:
        ua = UserAgent()
        req = Request(base_url + '?' + query_string, headers={'User-Agent': str(ua.chrome)})
        res = urlopen(req)
        html_data = BS(res.read(), 'html.parser')

        g_list = html_data.find_all('li', attrs={'class' : 'sh_blog_top'})
        try:
            urls = []
            times = []
            for g in g_list:
                time = g.find('dd', attrs={'class' : 'txt_inline'})
                url = g.find('a', attrs={'class' : 'url'})
                if url:
                    t = time.get_text()
                    times.append(t)
                    url_name = url.get_text().split('//')[-1]
                    urls.append(url_name)

            for i in range(0, len(urls)):
                if urls[i] == input_url:
                    rank = '%s위' %(i + 1)
                    time_ = times[i]
        except:
            traceback.print_exc()

    except:
        traceback.print_exc()
    return [rank, time_]


def mSearch(keyword, input_url):
    input_url = 'm.' + input_url # 모바일 버전의 url로 수정
    base_url = 'https://m.search.naver.com/search.naver'
    values = {
        'where' : 'm_view',
        'sm' : 'mtb_jum',
        'query' : keyword
    }

    query_string = parse.urlencode(values, encoding='UTF-8', doseq=True)
    context = ssl._create_unverified_context()
    rank = '순위 밖'
    url = ''
    time_ = ' '
    try:
        ua = UserAgent()
        req = Request(base_url + '?' + query_string, headers={'User-Agent': str(ua.chrome)})
        res = urlopen(req)
        html_data = BS(res.read(), 'html.parser')

        g_list = html_data.find_all('li', attrs={'class' : 'bx _item'})
        try:
            urls = []
            times = []
            for g in g_list:
                time = g.find('span', attrs={'class' : 'sub_time sub_txt'})
                url = g.find('a', attrs={'class' : 'api_txt_lines total_tit'})
                if url:
                    t = time.get_text()
                    times.append(t)
                    url_name = url['href']
                    url_name = url_name.split('//')[-1]
                    urls.append(url_name)

            for i in range(0, len(urls)):
                if urls[i] == input_url:
                    rank = '%s위' %(i + 1)
                    time_ = times[i]
        except:
            traceback.print_exc()

    except:
        traceback.print_exc()
    return [rank, time_]


@flask_app.route('/searchKeyword', methods = ['GET', 'POST'])
def search_keyword():
    if request.method != 'POST':
        return

    keyword = request.form['keyword']
    input_url = request.form['url'].split('//')[-1]
    if input_url.split('.')[0] == 'm':
        input_url = ".".join(input_url.split('.')[1:])

    print(input_url)
    print(keyword)

    web_rank, web_time = search(keyword, input_url)
    m_rank, m_time = mSearch(keyword, input_url)

    if web_time != " ":
        m_time = web_time
    elif m_time != " ":
        web_time = m_time

    if web_time == " " or m_time:
        web_time = getPostDate(input_url)
        m_time = web_time

    return render_template('index.html', url=input_url, keyword=keyword, web_rank=web_rank, web_time=web_time, m_rank=m_rank, m_time=m_time)


@flask_app.route('/')
def index():
    return render_template('index.html', url=" ", keyword=" ", rank=" ", time=" ")


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=54990)
