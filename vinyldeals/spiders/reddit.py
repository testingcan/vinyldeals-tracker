# -*- coding: utf-8 -*-
import scrapy
from vinyldeals.items import VinyldealsItem
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from vinyldeals.process import send_mail


class RedditSpider(scrapy.Spider):
    name = 'reddit'
    allowed_domains = ['reddit.com']
    start_urls = ['https://www.reddit.com/r/VinylDeals/new/?limit=100']

    def parse(self, response):
        item = VinyldealsItem()
        for sel in response.xpath('//body'):
            titles = sel.xpath('//a[@class="title may-blank outbound"]/text()').extract()
            urls = sel.xpath('//a[@class="title may-blank outbound"]/@href').extract()
        result = zip(titles, urls)
        for title, url in result:
            item["title"] = title
            item["url"] = url
            yield item

    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        send_mail()
