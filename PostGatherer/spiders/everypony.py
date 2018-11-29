# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from ..items import PostgathererItem

class EveryponySpider(CrawlSpider):
    name = 'everypony'
    allowed_domains = ['everypony.ru']
    start_urls = ['http://everypony.ru/']
    news_title_xpath = '//div[contains(@class, postItem)]/h2/a/'

    def __init__(self, category=None, news_title_xpath=None, *args, **kwargs):
        super(EveryponySpider, self).__init__(*args, **kwargs)
        if category:
            self.start_urls = ['https://everypony.ru/category/' % category]
        if news_title_xpath:
            self.news_title_xpath = news_title_xpath

    def parse(self, response):
        item = PostgathererItem()
        titles = self.parse_title(response)
        links = self.parse_link(response)
        for title, link in zip(titles, links):
            item['title'] = title
            item['link'] = link
            yield item

    def parse_title(self, response):
        return response.selector.xpath(self.news_title_xpath + 'text()').extract()

    def parse_link(self, response):
        return response.selector.xpath(self.news_title_xpath + '@href').extract()
