# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from douban3.items import *

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        #self.db[DoubanuserItem.collection].create_index([('id', pymongo.ASCENDING)])

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        #name = item.__class__.__name__
        #self.db[name].insert(dict(item))
        if isinstance(item, DoubanuserItem):
            self.db[item.collection].update({'id': item.get('id')}, {'$set': item}, True)
        if isinstance(item, UserRelationItem):
            self.db[item.collection].update(
                {'id': item.get('id')},
                {'$addToSet':
                    {
                        'contacts': {'$each': item['contacts']},
                        #'rev_contacts': {'$each': item['rev_contacts']}
                    }
                }, True)#用户

        if isinstance(item, DoubanMovietIdItem):
            self.db[item.collection].update(
                 {'id': item.get('id')},
                {'$addToSet':
                    {
                        'movie_id': item['movie_id']

                    }
                }, True)#用户-电影




        if isinstance(item, DoubanMusictIdItem):
            self.db[item.collection].update(
                 {'id': item.get('id')},
                 {'$addToSet':
                    {
                        'music_id': item['music_id']
                     }
                 }, True)#用户-音乐




        if isinstance(item, DoubanBookIdItem):
            self.db[item.collection].update(
                {'id': item.get('id')},
                {'$addToSet':
                    {
                        'book_id':  item['book_id']
                    }
                }, True)#用户-书籍

        return item

