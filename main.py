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
    if url.startswith('blog'):
        url = 'https://m.' + url 
    else:
        logNo = url.split('/')[-1]
        blogId = ''
        if url.split('.')[0] == 'dhaliaxjapan':
            blogId = 'dhaliaxjapan'
        elif url.split('.')[0] == 'misangu':
            blogId = 'musoi99'
        url = 'https://m.blog.naver.com/PostView.nhn?blogId=%s&logNo=%s'%(blogId, logNo)
        
    print(url)
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


def search_for_web(query_string, input_url):
    base_url = 'https://search.naver.com/search.naver'
    rank = 0
    url = ''
    try:
        ua = UserAgent()
        req = Request(base_url + '?' + query_string, headers={'User-Agent': str(ua.chrome)})
        res = urlopen(req)
        html_data = BS(res.read(), 'html.parser')

        g_list = html_data.find_all('li', attrs={'class' : 'sh_blog_top'})
        try:
            urls = []
            for g in g_list:
                url = g.find('a', attrs={'class' : 'url'})
                if url:
                    url_name = url.get_text().split('//')[-1]
                    urls.append(url_name)

            for i in range(0, len(urls)):
                if urls[i] == input_url:
                    rank = i + 1
        except:
            traceback.print_exc()

    except:
        traceback.print_exc()
    return rank


def search(keyword, input_url):
    values = {
        'where' : 'post',
        'sm' : 'tab_jum',
        'query' : keyword
    }
    query_string = parse.urlencode(values, encoding='UTF-8', doseq=True)
    rank = search_for_web(query_string, input_url)

    if rank is 0:
        values = {
            'where' : 'post',
            'sm' : 'tab_jum',
            'query' : keyword,
            'start' : '11'
        }
        query_string = parse.urlencode(values, encoding='UTF-8', doseq=True)
        if rank is 0:
            return '순위 밖'
        rank = search_for_web(query_string, input_url) + 10
    return '%s 위'%(rank)


def mSearch(keyword, input_url):
    input_url = 'm.' + input_url # 모바일 버전의 url로 수정
    base_url = 'https://m.search.naver.com/search.naver'
    values = {
        'where' : 'm_view',
        'sm' : 'mtb_jum',
        'query' : keyword
    }

    query_string = parse.urlencode(values, encoding='UTF-8', doseq=True)
    rank = '순위 밖'
    url = ''
    try:
        ua = UserAgent()
        req = Request(base_url + '?' + query_string, headers={'User-Agent': str(ua.chrome)})
        res = urlopen(req)
        html_data = BS(res.read(), 'html.parser')

        g_list = html_data.find_all('li', attrs={'class' : 'bx _item'})
        try:
            urls = []
            for g in g_list:
                url = g.find('a', attrs={'class' : 'api_txt_lines total_tit'})
                if url:
                    url_name = url['href']
                    url_name = url_name.split('//')[-1]
                    urls.append(url_name)

            for i in range(0, len(urls)):
                if urls[i] == input_url:
                    rank = '%s위' %(i + 1)
        except:
            traceback.print_exc()

    except:
        traceback.print_exc()
    return rank


@flask_app.route('/searchKeyword', methods = ['GET', 'POST'])
def search_keyword():
    if request.method != 'POST':
        return

    keyword = request.form['keyword']
    input_url = request.form['url'].split('//')[-1]
    if input_url.split('.')[0] == 'm':
        input_url = ".".join(input_url.split('.')[1:])

    print('%s : %s' %(keyword, input_url))

    web_rank = search(keyword, input_url)
    m_rank = mSearch(keyword, input_url)
    time = getPostDate(input_url)

    return render_template('index.html', url=input_url, keyword=keyword, web_rank=web_rank, web_time=time, m_rank=m_rank, m_time=time)


@flask_app.route('/')
def index():
    return render_template('index.html', url=" ", keyword=" ", rank=" ", time=" ")


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=54990)
