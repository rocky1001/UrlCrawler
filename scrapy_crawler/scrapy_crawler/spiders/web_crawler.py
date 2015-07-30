#coding=utf-8
from scrapy_crawler.items import WebItem
from scrapy import Request

__author__ = 'rockyqi1001@gmail.com'

from scrapy.spiders import Spider
from scrapy.selector import Selector
import logging


class WebSpider(Spider):
    name = "scrapy_test"

    # start_urls = [
    #     # "http://news.163.com/13/0708/10/938MALOV00014AED.html",
    #     # "http://news.163.com/13/0708/11/938Q3F1N00014Q4P.html",
    #     # "http://news.163.com/13/0708/18/939J3DUP00014JB6.html",
    #     # "http://news.163.com/13/0708/20/939MV02300014JB5.html",
    #     # "http://news.163.com/13/0709/06/93AQ5K3H00014AED.html",
    #     # "http://news.163.com/13/0709/06/93AQMR8J00014Q4P.html?_t=t",
    #     "http://news.163.com/13/0709/15/93BQE6UL00014JB6_all.html",
    #     # "http://news.163.com/13/0710/06/93DEULTV00014Q4P.html",
    #     # "http://news.163.com/13/0710/08/93DJFGTS00014Q4P.html",
    # ]

    def start_requests(self):
        with open('urls_3k.txt', 'r') as urls:
            for url in urls:
                yield Request(url, self.parse)

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html
        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        logging.debug('response.encoding=' + response.encoding)

        sel = Selector(response)
        item = WebItem()
        item['url'] = response.url
        item['title'] = sel.xpath('//title/text()').extract()
        item['keywords'] = sel.xpath("//meta[@name='keywords']/@content | //meta[@name='Keywords']/@content | //meta[@name='keyword']/@content").extract()
        item['description'] = sel.xpath("//meta[@name='description']/@content | //meta[@name='Description']/@content | //meta[@name='descriptions']/@content").extract()

        logging.debug('title=' + item['title'][0])
        return item