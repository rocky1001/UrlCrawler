#coding=utf-8
__author__ = 'rocky'
import scrapy
import requests
from bs4 import BeautifulSoup
from scrapy.spider import BaseSpider

ORIGIN_DATA_FILE = 'urls_test_10.txt'
TIME_OUT = 3

RESULT_FILE = 'result_' + ORIGIN_DATA_FILE

def crawl_urls_file(test_url=None):
    pass


def do_crawl(url):
    try:
        if not url.startswith('http://'):
            url = 'http://{0}'.format(url)
        print url
        segment_result = str()
        resp = requests.get(url, timeout=TIME_OUT)
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
                title_data = bs.title.get_text().strip().encode('utf-8')
                segment_result += " ".join(jieba.lcut(title_data))
            else:
                title_data = 'NoTitle'

            all_p_tag = bs.find_all("p")
            for p_tag in all_p_tag:
                # print p_tag
                tag_data = p_tag.text.strip().replace('\n', '').encode('utf-8')
                segment_result += " ".join(jieba.lcut(tag_data))

            # all_div_tag = bs.find_all("div")
            # for div_tag in all_div_tag:
            #     # print p_tag
            #     div_data = div_tag.text.strip().replace('\n', '').encode('utf-8')
            #     segment_result += " ".join(jieba.lcut(div_data))

        else:
            segment_result += 'NoConnection'
    except Exception, e:
        print url, e.message
        segment_result += 'Error'

    # print segment_result
    return segment_result.encode('utf-8')


if __name__ == '__main__':
    print 'Crawler begin...'

    test_url = 'http://www.haibao.com/article/199564.htm'
    crawl_urls_file()

    print 'Crawler finished successfully.'
