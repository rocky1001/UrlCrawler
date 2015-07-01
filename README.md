# UrlCrawler
Author rocky.chi<mailto:rockychi1001@gmail.com>

## Advantage 
Using requests and beautifulsoup4 to crawl and parse html data;
Handle chinese characters smartly, avoid gibberish characters(中文乱码).

## version 0.0.1
Title spider can crawl urls according to existed url file, parse and get data in \<title>\</title> block,
then return the new result file with **title data** added.

## version 0.0.2
Price spider added.
Using selenium (or phantomjs) to crawl **price** element of the specified host (eg:jd.com, tmall.com),
because the price element is load by js asynchronously in the page.


