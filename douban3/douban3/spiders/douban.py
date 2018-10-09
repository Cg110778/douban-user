# -*- coding: utf-8 -*-
import pymongo
import re

import scrapy
from scrapy import Request,Spider
from douban3.items import *

class DoubanSpider(Spider):
    name = 'douban3'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/people/{uid}/']
    contacts_url= 'https://www.douban.com/people/{uid}/contacts'
    user_url = 'http://douban.com/people/{uid}/'
    start_users = ['pongba'] #'pongba''57109633',#'1693422','50446886'ninetonine''137546285'183501886'#'3452208'新桥，宋史
    movie_do_url = 'https://movie.douban.com/people/{uid}/do'
    movie_wish_url = 'https://movie.douban.com/people/{uid}/wish'
    movie_collect_url = 'https://movie.douban.com/people/{uid}/collect'
    music_do_url = 'https://music.douban.com/people/{uid}/do'
    music_wish_url = 'https://music.douban.com/people/{uid}/wish'
    music_collect_url = 'https://music.douban.com/people/{uid}/collect'
    book_do_url = 'https://book.douban.com/people/{uid}/do'
    book_wish_url = 'https://book.douban.com/people/{uid}/wish'
    book_collect_url = 'https://book.douban.com/people/{uid}/collect'
    contacts_id=[]


    def get_contacts(self, collection, database):
        client = pymongo.MongoClient('localhost', 27017)
        db = client[database]
        collection = db[collection]
        dbcontacts = collection.find({'id':'pongba'}, {'_id': 0, 'contacts': 1})
        return dbcontacts

    def start_requests(self):
        for uid in self.start_users:
            yield Request(self.user_url.format(uid=uid), callback=self.parse_user)


    def parse_user(self,response):
        item=DoubanuserItem()
        item['id'] = response.xpath(
            '//*[@id="profile"]//div[@class="basic-info"]//div[@class="user-info"]//div[@class="pl"]/text()').re_first(
            '(\S+)')
        item['url']=response.url
        item['name'] = ''.join(
            response.xpath('//*[@id="db-usr-profile"]/div[@class="info"]/h1/text()').extract()).strip()
        item['img'] = response.xpath('//*[@id="profile"]//div[@class="basic-info"]/img/@src').extract_first()
        item['habitual_residence'] = response.xpath(
            '//*[@id="profile"]//div[@class="user-info"]/a/text()').extract_first()
        item['record_date'] = response.xpath(
            '//*[@id="profile"]//div[@class="basic-info"]//div[@class="user-info"]//div[@class="pl"]/text()').re_first(
            '(.*?)加入')
        item['user_display'] = ','.join(response.xpath(
            '//*[@id="profile"]//div[@class="user-intro"]//span[@id="intro_display"]/text()').extract()).strip()
        #contacts_count=response.xpath('//*[@id="friend"]//span[@class="pl"]/a/text()').re_first('成员(\d+)')
        item['contacts_count'] = response.xpath('//*[@id="friend"]//span[@class="pl"]/a/text()').re_first('成员(\d+)')
        item['rev_contacts_count'] = response.xpath('//*[@class="rev-link"]/a/text()').re_first('.*?被(\d+)人关注')
        item['movie_do_number'] = response.selector.re_first(re.compile(
            '.*?<a href="https://movie.douban.com/people/.*?/do" target="_blank">(.*?在看)</a>'))
        item['movie_wish_number'] = response.selector.re_first(re.compile(
            '.*?<a href="https://movie.douban.com/people/.*?/wish" target="_blank">(.*?想看)</a>'))
        item['movie_collect_number'] = response.selector.re_first(re.compile(
            '.*?<a href="https://movie.douban.com/people/.*?/collect" target="_blank">(.*?看过)</a>'))
        item['music_do_number'] = response.selector.re_first(re.compile(
            '.*?<a href="https://music.douban.com/people/.*?/do" target="_blank">(.*?在听)</a>'))
        item['music_wish_number'] = response.selector.re_first(re.compile(
            '.*?<a href="https://music.douban.com/people/.*?/wish" target="_blank">(.*?想听)</a>'))
        item['music_collect_number'] = response.selector.re_first(re.compile(
            '.*?<a href="https://music.douban.com/people/.*?/collect" target="_blank">(.*?听过)</a>'))
        item['book_do_number'] = response.selector.re_first(re.compile(
            '.*?<a href="https://book.douban.com/people/.*?/do" target="_blank">(.*?在读)</a>'))
        item['book_wish_number'] = response.selector.re_first(re.compile(
            '.*?<a href="https://book.douban.com/people/.*?/wish" target="_blank">(.*?想读)</a>'))
        item['book_collect_number'] = response.selector.re_first(re.compile(
            '.*?<a href="https://book.douban.com/people/.*?/collect" target="_blank">(.*?读过)</a>'))
        item['review_number']=response.xpath('//div[@id="review"]//span[@class="pl"]/a/text()').extract_first()
        yield item
        uid = response.xpath(
            '//*[@id="profile"]//div[@class="basic-info"]//div[@class="user-info"]//div[@class="pl"]/text()').re_first(
            '(\S+)')
        yield Request(self.contacts_url.format(uid=uid), callback=self.parse_contacts_list)
        
        yield Request(self.movie_do_url.format(uid=uid), callback=self.parse_movie_link)
        #yield Request(self.movie_wish_url.format(uid=uid), callback=self.parse_movie_link)
        yield Request(self.movie_collect_url.format(uid=uid), callback=self.parse_movie_link)
        yield Request(self.music_do_url.format(uid=uid), callback=self.parse_music_link)
        #yield Request(self.music_wish_url.format(uid=uid), callback=self.parse_music_link)
        yield Request(self.music_collect_url.format(uid=uid), callback=self.parse_music_link)
        yield Request(self.book_do_url.format(uid=uid), callback=self.parse_book_link)
        #yield Request(self.book_wish_url.format(uid=uid), callback=self.parse_book_link)
        yield Request(self.book_collect_url.format(uid=uid), callback=self.parse_book_link)#起点用户'''
        '''dbcontacts_count = self.get_contacts(collection='users', database='new_douban')
        if dbcontacts_count:
            for contact in dbcontacts_count:
                contact=contact['contacts']
                for i in contact:
                    uid=i['id']

        
        #uid=response.xpath('//*[@id="profile"]//div[@class="basic-info"]//div[@class="user-info"]//div[@class="pl"]/text()').re_first('(\S+)')
                    yield Request(self.user_url.format(uid=uid), callback=self.parse_user)
                    yield Request(self.contacts_url.format(uid=uid), callback=self.parse_contacts_list)
                    yield Request(self.movie_do_url.format(uid=uid), callback=self.parse_movie_link)
                    #yield Request(self.movie_wish_url.format(uid=uid), callback=self.parse_movie_link)
                    yield Request(self.movie_collect_url.format(uid=uid), callback=self.parse_movie_link)
                    yield Request(self.music_do_url.format(uid=uid), callback=self.parse_music_link)
                    #yield Request(self.music_wish_url.format(uid=uid), callback=self.parse_music_link)
                    yield Request(self.music_collect_url.format(uid=uid), callback=self.parse_music_link)
                    yield Request(self.book_do_url.format(uid=uid), callback=self.parse_book_link)
                    #yield Request(self.book_wish_url.format(uid=uid), callback=self.parse_book_link)
                    yield Request(self.book_collect_url.format(uid=uid), callback=self.parse_book_link)#数据库里的用户'''


    def parse_contacts_list(self, response):
        user_realation_item = UserRelationItem()
        #contacts_count=int(response.meta['contacts_count'])
        #print(contacts_count)
        result = re.search('https://www.douban.com/people/(.*?)/contacts', response.url)
        uid = result.group(1)
        contacts_list = response.xpath('//*[@id="content"]//div[@class="article"]//dl[@class="obu"]')
        for contact in contacts_list:
            contact_id = contact.xpath('./dd/a/@href').re_first('https://www.douban.com/people/(.*?)/')
            self.contacts_id.append(contact_id)
            name = contact.xpath('./dd/a/text()').extract_first()
            contacts = [{'id': contact_id, 'name': name}]
            user_realation_item['id'] = uid
            user_realation_item['contacts'] = contacts
            yield user_realation_item
            #if len(self.contacts_id)>contacts_count:
                #return ''
            #else:
                #yield Request(self.user_url.format(uid=contact_id),callback=self.parse_user)

    def parse_movie_link(self,response):
        id = response.xpath('//*[@id="db-usr-profile"]/div[@class="info"]//li[1]/a/@href').extract_first()
        id = re.search('.*?/people/(.*?)/', id)
        id = id.group(1)
        movie_link=response.xpath(
            '//*[@id="content"]//div[@class="article"]//a[@class="nbg"]/@href').extract()
        #电影链接
        for i in movie_link:
            item=DoubanMovietIdItem()
            movie_id = re.search('https://movie.douban.com/subject/(.*?)/', i)
            movie_id = movie_id.group(1)
            item['movie_id'] = movie_id
            item['id'] = id
            yield item
            next_page = response.xpath(
                '//*[@id="content"]//div[@class="paginator"]/span[@class="next"]//a[contains(.,"后页")]/@href').extract_first()
            if next_page:
               if 'douban.com' in next_page:
                   yield Request(url=next_page, callback=self.parse_movie_link)
               else:
                    next_page_url = 'https://movie.douban.com' + next_page
                    # print(next_page,response.url)
                    yield Request(url=next_page_url, callback=self.parse_movie_link)
                    # 下一页subject列表'''


    def parse_music_link(self, response):
        id = response.xpath('//*[@id="db-usr-profile"]/div[@class="info"]//li[1]/a/@href').extract_first()
        id = re.search('.*?/people/(.*?)/', id)
        id = id.group(1)
        music_link = response.xpath('//*[@id="content"]//div[@class="article"]//a[@class="nbg"]/@href').extract()
        # 音乐链接
        for i in music_link:
            item = DoubanMusictIdItem()
            music_id = re.search('https://music.douban.com/subject/(.*?)/', i)
            music_id = music_id.group(1)
            item['music_id'] = music_id
            item['id'] = id
            yield item
            next_page = response.xpath(
                '//*[@id="content"]//div[@class="paginator"]/span[@class="next"]//a[contains(.,"后页")]/@href').extract_first()
            if next_page:
                if 'douban.com' in next_page:
                    yield Request(url=next_page, callback=self.parse_music_link)
                else:
                    next_page_url = 'https://music.douban.com' + next_page
                    yield Request(url=next_page_url, callback=self.parse_music_link)
                    # 下一页subject列表'''

    def parse_book_link(self, response):
        id = response.xpath('//*[@id="db-usr-profile"]/div[@class="info"]//li[1]/a/@href').extract_first()
        id = re.search('.*?/people/(.*?)/', id)
        id = id.group(1)
        book_link = response.xpath('//*[@id="content"]//div[@class="article"]//a[@class="nbg"]/@href').extract()
        # 书籍链接
        for i in book_link:
            item = DoubanBookIdItem()
            book_id = re.search('https://book.douban.com/subject/(.*?)/', i)
            book_id = book_id.group(1)
            item['book_id'] = book_id
            item['id'] = id
            yield item
            next_page = response.xpath(
                '//*[@id="content"]//div[@class="paginator"]/span[@class="next"]//a[contains(.,"后页")]/@href').extract_first()
            if next_page:
                if 'douban.com' in next_page:
                    yield Request(url=next_page, callback=self.parse_book_link)
                else:
                    next_page_url = 'https://book.douban.com' + next_page
                    yield Request(url=next_page_url, callback=self.parse_book_link)
                    # 下一页subject列表'''








