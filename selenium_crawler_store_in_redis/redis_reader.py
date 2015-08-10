#coding=utf-8
__author__ = 'rockychi1001@gmail.com'


import redis

ORIGIN_FILE = 'site_urls.txt'
RESULT_FILE = 'result_site_urls.txt'

rs = redis.StrictRedis(host='192.168.8.1', port=6379, db=0)

result_dict = dict()
with open(ORIGIN_FILE, 'r') as origin_url_file:
    for url in origin_url_file:
        if not url.startswith('http://'):
            url = 'http://{0}'.format(url)
        result_dict[url.replace('\n', '')] = rs.get(url.replace('\n', ''))

# print result_dict

with open(RESULT_FILE, 'w') as result_data_file:
    for url, result in result_dict.items():
        if result is None:
            continue
        result_data_file.write(url.replace('\n', ''))
        result_data_file.write('||')
        result_data_file.write(result)
        result_data_file.write('\n')
