# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    positionName = Field()
    companyFullName = Field()
    salary = Field()
    createTime = Field()
    company_content = Field()
    job_advantage = Field()
    job_addr = Field()
    
