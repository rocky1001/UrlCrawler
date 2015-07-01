# UrlCrawler
Author rocky.chi<mailto:rockychi1001@gmail.com>

## Function
1.Title spider, using requests and beautifulsoup4 to crawl and parse html data;
handle chinese characters smartly, avoid gibberish chinese characters(中文乱码).

2.Price spider, using selenium driver to start chrome or firefox (phantomjs will do the same work);
crawling element loaded by js asynchronously in the page, such as **price**.

## version 0.0.1
Title spider can crawl urls according to existed url file, parse and get data in \<title>\</title> block,
then return the new result file with **title data** added.

## version 0.0.2
Price spider added.
Using selenium (or phantomjs) to crawl **price** element of the specified host (eg:jd.com, tmall.com),
because the price element is load by js asynchronously in the page.


