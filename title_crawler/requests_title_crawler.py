#coding=utf-8
__author__ = 'rocky'
import requests
from bs4 import BeautifulSoup

ORIGIN_DATA_FILE = 'urls.txt'
TIME_OUT = 1

RESULT_FILE = 'result_' + ORIGIN_DATA_FILE
HEADERS = {
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/40.0.2214.93 Safari/537.36',
    'DNT': '1',
    'Accept-Encoding': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,en-US;q=0.2',
    'Cache-Control': 'max-age=0'
}


def crawl_urls_file():
    title_result = dict()
    result_data = list()
    try:
        with open(ORIGIN_DATA_FILE, 'r') as url_file:
            for url in url_file:
                clean_data = url.replace('\n', '')
                if title_result.get(url) is not None:
                    continue
                title = do_crawl(url)
                title = title.encode('utf-8').strip()
                title_result[url] = title
                result_data.append(clean_data + '||' + title)
                result_data.append('\n')
                print url, title_result.get(url)

        if result_data:
            with open(RESULT_FILE, 'w') as result_data_file:
                result_data_file.writelines(result_data)
    except Exception, e:
        print "ERROR:[%s]" % e.message


def do_crawl(url):
    try:
        if not url.startswith('http://'):
            url = 'http://{0}'.format(url)
        resp = requests.get(url, timeout=TIME_OUT, headers=HEADERS)
        if resp.ok and resp.content is not None:

            charset = requests.utils.get_encodings_from_content(resp.content)
            if len(charset) > 0:
                resp.encoding = charset[0]
                bs = BeautifulSoup(resp.text)
            else:
                bs = BeautifulSoup(resp.content, from_encoding='gb18030')

            if bs.title is not None and bs.title.get_text() is not None \
                    and bs.title.get_text().strip() is not '' \
                    and bs.title.get_text().strip() is not u'':
                # return bs.title.string
                return bs.title.get_text().strip()
            else:
                return 'no title'
        else:
            return 'no connection'
    except Exception, e:
        print url, e.message
        return 'no connection'


if __name__ == '__main__':
    print 'Crawler begin...'

    crawl_urls_file()

    # print do_crawl('www.dianping.com')

    print 'Crawler finished successfully.'
