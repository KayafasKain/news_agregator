# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import motor.motor_asyncio
import asyncio
from scrapy.utils.serialize import ScrapyJSONEncoder
_encoder = ScrapyJSONEncoder()
MONGO_CLIENT = motor.motor_asyncio.AsyncIOMotorClient(
    'mongodb://Admin1:Admin1@ds129926.mlab.com:29926/news_aggregator'
).news_aggregator

class PostgathererPipeline(object):
    db = MONGO_CLIENT
    async def insert_item(self, spider, item):
        await self.db[spider.name].update_one(item, {'$set': item}, upsert=True)

    def process_item(self, item, spider):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.insert_item(spider, dict(item)))
        return item