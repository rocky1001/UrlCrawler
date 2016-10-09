#coding=utf-8
__author__ = 'rocky'
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

CHROME_DRIVER_PATH = 'D:/software/google/chromedriver.exe'
ORIGIN_DATA_FILE = 'urls_3k.txt'
TIME_OUT = 3

RESULT_FILE = 'result_' + ORIGIN_DATA_FILE


def crawl_urls_file(_test_url=None):
    if _test_url:
        print do_crawl(_test_url)
    else:
        result_data = list()
        with open(ORIGIN_DATA_FILE, 'r') as url_file:
            url_data = url_file.readlines()
            for index, url in enumerate(url_data):
                result_data.append(do_crawl(url.replace('\n', '')))
                print 'crawling no.', index

        if result_data:
            with open(RESULT_FILE, 'w') as result_data_file:
                for url, result in zip(url_data, result_data):
                    result_data_file.write(url.replace('\n', ''))
                    result_data_file.write('||')
                    result_data_file.write(result)
                    result_data_file.write('\n')


def do_crawl(url):
    try:
        if not url.startswith('http://'):
            url = 'http://{0}'.format(url)
        # print url
        result = str()

        resp = DRIVER.get(url)
        DRIVER.implicitly_wait(2)
        html_data = DRIVER.page_source
        # if resp.content is not None:
        if html_data is not None:
            charset = requests.utils.get_encodings_from_content(html_data)
            if len(charset) > 0:
                bs = BeautifulSoup(html_data, from_encoding=charset)
            else:
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
            result += '$$$'

            content_data = str()
            all_p_tag = bs.find_all("p")
            for p_tag in all_p_tag:
                # print p_tag
                tag_data = p_tag.text.strip().replace('\n', '').encode('utf-8')
                content_data += tag_data

            result += 'content=' + content_data
            result += '$$$'

            # all_div_tag = bs.find_all("div")
            # for div_tag in all_div_tag:
            #     # print p_tag
            #     div_data = div_tag.text.strip().replace('\n', '').encode('utf-8')
            #     segment_result += " ".join(jieba.lcut(div_data))

        else:
            result += 'NoConnection'
            # DRIVER.close()
    except Exception, e:
        print url, e.message
        result += 'Error'
        # DRIVER.close()

    # print result
    return result


if __name__ == '__main__':
    print 'Crawler begin...'
    test_url = 'http://news.163.com/13/0709/15/93BQE6UL00014JB6_all.html'

    # 1.use block image tool
    # chromeOptions = webdriver.ChromeOptions()
    # chromeOptions.add_extension("Block-image_v1.1.crx")

    # 2.use chrome options
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chromeOptions.add_experimental_option("prefs", prefs)

    DRIVER = webdriver.Chrome(CHROME_DRIVER_PATH, chrome_options=chromeOptions)
    # DRIVER.set_page_load_timeout(TIME_OUT)
    crawl_urls_file(test_url)
    DRIVER.close()

    print 'Crawler finished successfully.'
