#coding=utf-8
import redis

__author__ = 'rockychi1001@gmail.com'
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

CHROME_DRIVER_PATH = 'D:/software/google/chromedriver.exe'
ORIGIN_DATA_FILE = 'site_urls.txt'
TIME_OUT = 3


def crawl_urls_file(_test_url=None):
    if _test_url:
        print do_crawl_and_save(_test_url)
    else:
        rs = redis.StrictRedis(host='192.168.8.1', port=6379, db=0)
        with open(ORIGIN_DATA_FILE, 'r') as url_file:
            url_data = url_file.readlines()
            for index, url in enumerate(url_data):
                do_crawl_and_save(url.replace('\n', ''), rs)
                print 'crawling no.', index


def do_crawl_and_save(url, rs=None):
    try:
        if not url.startswith('http://'):
            url = 'http://{0}'.format(url)
        # check duplicate url
        if rs is not None and rs.get(url) is not None:
            return

        result = str()
        DRIVER.get(url)
        html_data = DRIVER.page_source
        # if resp.content is not None:
        if html_data is not None:
            # charset = requests.utils.get_encodings_from_content(resp.content)
            charset = requests.utils.get_encodings_from_content(html_data)
            if len(charset) > 0:
                # resp.encoding = charset[0]
                # bs = BeautifulSoup(resp.text)
                bs = BeautifulSoup(html_data, from_encoding=charset)
            else:
                # bs = BeautifulSoup(resp.content, from_encoding='gb18030')
                bs = BeautifulSoup(html_data, from_encoding='gb18030')

            if bs.title is not None and bs.title.get_text() is not None \
                    and bs.title.get_text().strip() is not '' \
                    and bs.title.get_text().strip() is not u'':
                # return bs.title.string
                title_data = bs.title.get_text().strip().encode('utf-8')
            else:
                title_data = ''

            result += 'title=' + title_data
            result += '$$$'

            keyword_data = str()
            all_meta_tag = bs.find_all(attrs={"name": "keywords"})
            for meta_tag in all_meta_tag:
                # print p_tag
                tag_data = meta_tag['content'].strip().replace('\n', '').encode('utf-8')
                keyword_data += tag_data

            result += 'keywords=' + keyword_data
            result += '$$$'

            description_data = str()
            all_meta_tag = bs.find_all(attrs={"name": "description"})
            for meta_tag in all_meta_tag:
                # print p_tag
                tag_data = meta_tag['content'].strip().replace('\n', '').encode('utf-8')
                description_data += tag_data

            result += 'description=' + description_data

        else:
            result += 'Error'
    except Exception, e:
        print url, e.message
        result += 'Error'

    # save result
    if rs is not None:
        if result.find('Error') == -1:
            rs.set(url, result)
    else:
        return result


if __name__ == '__main__':
    print 'Crawler begin...'
    test_url = 'http://news.163.com/13/0709/15/93BQE6UL00014JB6_all.html'

    # setup = "from __main__ import crawl_urls_file"
    # print timeit.timeit("crawl_urls_file('http://config.qc188.com/m9991/ca13/')", setup=setup, number=1)

    chromeOptions = webdriver.ChromeOptions()
    # chromeOptions.add_extension("Block-image_v1.1.crx")

    chromeOptions = webdriver.ChromeOptions()
    # disable image loading
    prefs = {"profile.managed_default_content_settings.images": 2}
    chromeOptions.add_experimental_option("prefs", prefs)

    # disable flash
    chromeOptions.add_argument("--disable-bundled-ppapi-flash")

    chromeOptions.add_argument("--disable-plugins-discovery")
    chromeOptions.add_argument("--disable-internal-flash")

    DRIVER = webdriver.Chrome(CHROME_DRIVER_PATH, chrome_options=chromeOptions)
    # DRIVER.set_page_load_timeout(TIME_OUT)
    DRIVER.implicitly_wait(2)
    crawl_urls_file()
    DRIVER.close()

    print 'Crawler finished successfully.'
