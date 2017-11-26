# -*- coding: utf-8 -*-

from vinyldeals.models import Deal, session

class VinyldealsPipeline(object):
    def process_item(self, item, spider):
        # Checks if deal already exists in DB and adds it if not
        new_deal = Deal(title=item["title"], url=item["url"])
        deal = session.query(Deal).filter_by(title=new_deal.title).first()
        if deal is None:
            session.add(new_deal)
            session.commit()
