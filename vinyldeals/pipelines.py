# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from vinyldeals.models import Deal, session

class VinyldealsPipeline(object):
    def process_item(self, item, spider):
        deal = Deal(title=item["title"], url=item["url"])
        session.add(deal)
        session.commit()
        return item
