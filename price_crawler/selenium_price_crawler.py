#coding=utf-8
__author__ = 'rocky'
import time

from selenium import webdriver

# using chrome driver to start chrome and do price_crawl
CHROME_DRIVER_PATH = 'XXX/google/chromedriver.exe'
# using phantomjs driver to do price_crawl(does not need any explorer to be opened)
PHANTOMJS_DRIVER_PATH = 'XXX/phantomjs-2.0.0/bin/phantomjs.exe'
URL_FILE_PATH = 'urls.txt'
URL_RESULT_PATH = 'result.txt'
WAIT_TIME = 3


def read_file2dict():
    origin_url_list = list()
    with open(URL_FILE_PATH, 'r') as url_file:
        for line in url_file:
            line = line.strip(' ').strip('\n')
            origin_url_list.append(line)
    return origin_url_list


def write_dict2file(_url_result_list):
    with open(URL_RESULT_PATH, 'w') as result_file:
        result_file.writelines(_url_result_list)


def get_price_by_selenium(_driver, _url_list):
    result_list = list()
    for url_line in _url_list:
        _driver.get(url_line)
        time.sleep(WAIT_TIME)  # Let the user actually see something!
        try:
            if 'jd.com' in url_line:
                kws = _driver.find_elements_by_id('jd-price')
            elif 'tmall.com' in url_line:
                kws = _driver.find_elements_by_class_name('tm-price')
            else:
                print 'URL not supported.'
                result_list.append(url_line + ',' + 'URL not supported.' + '\n')
                continue

            print url_line + ',' + unicode(kws[0].text).replace(u'￥', u'')
            result_list.append(url_line + ',' + unicode(kws[0].text).replace(u'￥', u'') + '\n')
        except Exception, e:
            print "Can't find price element."
            result_list.append(url_line + ',' + "Can't find price element." + '\n')
            continue
    return result_list


if __name__ == '__main__':
    url_list = read_file2dict()

    # driver = webdriver.Chrome(CHROME_DRIVER_PATH)

    # driver = webdriver.PhantomJS(PHANTOMJS_DRIVER_PATH)
    # url_result_list = get_price_by_selenium(driver, url_list)
    # driver.quit()

    # service = service.Service('D:/software/google/chromedriver.exe')
    # service.start()
    # capabilities = {'chrome.binary': 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'}
    # driver = webdriver.Remote(service.service_url, capabilities)
    # get_price_by_selenium(driver)
    # driver.quit()

    # write_dict2file(url_result_list)