
from scrapy import Spider
#from scrapy.http import Request
from bs4 import BeautifulSoup as bs
#import re
from zhilian_crawler.items import ZhilianCrawlerItem

class ZhilianSpider(Spider):
    name = 'zhilian_crawler_spider'
    start_urls = [
                  "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%8C%97%E4%BA%AC&kw=python%E7%88%AC%E8%99%AB%E5%B7%A5%E7%A8%8B%E5%B8%88&p=1&isadv=0",
                ]
    def parse(self,response):
        soup = bs(response.text,'lxml')
        item = ZhilianCrawlerItem()
        job_total = soup.find('div',attrs={'id':'newlist_list_content_table'})
        for job in job_total.find_all('table',attrs={'class':'newlist'})[1:]:
            item['company_name'] = job.find('td',attrs={'class':'zwmc'}).text.strip()
            item['salary'] = job.find('td',attrs={'class':'gsmc'}).text.strip()
            item['job_title'] = job.find('td',attrs={'class':'zwyx'}).text.strip()
            item['address'] = job.find('td',attrs={'class':'gzdd'}).text.strip()
            yield item

