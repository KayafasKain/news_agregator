import asyncio
import logging
import motor.motor_asyncio
from scrapy.utils.serialize import ScrapyJSONEncoder
_encoder = ScrapyJSONEncoder()


class DBOperator(object):

    loop = asyncio.get_event_loop()

    def __init__(self, db, limit=10):
        self.db = db
        self.limit = 10
        self.connection_test()

    def connection_test(self):
        self.loop.run_until_complete(self.get_fresh_items())


    def execute_task(self, method):
        result = self.loop.run_until_complete(method)
        if result:
            return result

    async def create_subscriber(self, subscriber, collection='subscribers'):
        await self.db[collection].update_one(subscriber, { '$set': subscriber }, upsert=True)

    async def update_subscriber(self, subscriber, collection='subscribers'):
        await self.db[collection].update_one({'chat_id': subscriber['chat_id'] }, { '$set': subscriber }, upsert=True)

    async def find_subscriber(self, chat_id, collection='subscribers'):
        return await self.db[collection].find_one({'chat_id': chat_id})

    async def get_interested_subscribers(self, preferneces):
        pass

    async def update_item(self, item, collection='everypony'):
        await self.db[collection].update_one(item, {'$set': {'brodcasted': True}}, upsert=True)

    async def get_fresh_items(self, collection='everypony'):
        fresh_items = self.db[collection].find({'broadcasted': { '$ne': True}})
        result_list =[]
        for item in await fresh_items.to_list(length=self.limit):
            await self.update_item(item, collection=collection)
            result_list.append(item)
        return result_list

    async def get_last_items(self, limit=10, collection='everypony'):
        return await self.db[collection].find().limit(limit)

