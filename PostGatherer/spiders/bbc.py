# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from ..items import PostgathererItem

class BbcSpider(CrawlSpider):
    name = 'bbc'
    start_urls = ['https://www.bbc.com/news']
    news_section_xpath = '//div[contains(@class, nw-c-top-stories--international)]'
    news_title_xpath = '//h2/..//h3'
    news_link_xpath = '//h2/..//div/a[contains(@class, nw-o-link-split__anchor)]'
    link_prefix = 'https://www.bbc.com'

    def __init__(self, category=None, news_title_xpath=None, *args, **kwargs):
        super(BbcSpider, self).__init__(*args, **kwargs)
        if category:
            self.start_urls = ['https://www.bbc.com/' % category]
        if news_title_xpath:
            self.news_title_xpath = news_title_xpath

    def parse(self, response):
        item = PostgathererItem()
        titles = self.parse_title(response)[1:]
        links = self.parse_link(response)[1:]
        for title, link in zip(titles, links):
            item['title'] = title
            if 'https'not in link:
                link = self.link_prefix + link
            item['link'] = link
            yield item

    def parse_title(self, response):
        return response.selector.xpath(self.news_section_xpath + self.news_title_xpath + '/text()').extract()

    def parse_link(self, response):
        return response.selector.xpath(self.news_section_xpath + self.news_link_xpath + '/@href').extract()
