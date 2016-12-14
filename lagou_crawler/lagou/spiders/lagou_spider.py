#coding:utf-8
from scrapy import Spider
from scrapy.http import Request
from bs4 import BeautifulSoup as bs
import json
from lagou.items import LagouItem

class LagouSpider(Spider):
    name = 'lagou'
    base_url = 'http://www.lagou.com/jobs/positionAjax.json?city=%e5%85%a8%e5%9b%bd&first=true&kd=%3d%e7%88%ac%e8%99%ab&pn='
    start_urls = []
    for i in range(1,24):
        full_url = base_url+str(i)
        start_urls.append(full_url)
    
    def parse(self,response):
        meta = {}
        soup = bs(response.body,'lxml')
        jsondata = json.loads(soup.body.text,encoding='utf-8')
        dictdata = dict(jsondata)
        for i in dictdata['content']['positionResult']['result']:
            #get some job info
            company_id = i['companyId'] 
            company_url = 'https://www.lagou.com/gongsi/'+str(company_id)+'.html'
            job_id = i['positionId']
            meta['job_url'] = 'https://www.lagou.com/jobs/'+str(job_id)+'.html'
            meta['positionName'] = i['positionName']
            meta['companyFullName'] = i['companyFullName']
            meta['salary'] = i['salary']
            meta['createTime'] = i['createTime']
            yield Request(url=company_url,callback = self.parse_company_info,meta=meta)
            
    def parse_company_info(self,response):
        soup = bs(response.body,'lxml')
        response.meta['company_content'] = soup.find('span',attrs={'class':'company_content'}).text.strip()
        
        yield Request(url=response.meta['job_url'],callback = self.parse_job_detail,meta=response.meta)
        
    def parse_job_detail(self,response):
        soup = bs(response.body,'lxml')
        response.meta['job_advantage'] = soup.find('dd',attrs={'class':'job-advantage'}).text.\
        encode('utf-8').split('：')[1].strip()
    
        response.meta['job_addr'] = soup.find('div',attrs={'class':'work_addr'}).text.strip().replace(' ','').\
        replace('\n','').encode('utf-8').replace('查看地图','')
        
        item = LagouItem()
        item['positionName'] = response.meta['positionName']
        item['companyFullName'] = response.meta['companyFullName']
        item['salary'] = response.meta['salary']
        item['createTime'] = response.meta['createTime']
        item['company_content'] = response.meta['company_content']
        item['job_advantage'] = response.meta['job_advantage']
        item['job_addr'] = response.meta['job_addr']
        yield item