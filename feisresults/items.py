# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FeisresultsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    feis = scrapy.Field()
    date = scrapy.Field()
    year = scrapy.Field()
    #month = scrapy.Field()
    #days = scrapy.Field()
    name = scrapy.Field()
    school = scrapy.Field()
    region = scrapy.Field()
    place = scrapy.Field()
    competition = scrapy.Field()
    wq = scrapy.Field()
    wmh = scrapy.Field()

