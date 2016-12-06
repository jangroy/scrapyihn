# -*- coding: utf-8 -*-
import scrapy
from scrapy.item import Item
from scrapy_splash import SplashRequest
from rasplayer.defaults import DefaultLoader, IndexItemSpider
from w3lib.html import remove_tags
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity, Compose


class CustomLoader(DefaultLoader):
    name_in = MapCompose(remove_tags, unicode.strip, unicode.upper)


def items_selector(s, r):
    return r.css('li.item')


def item_url_selector(s, i):
    i.css('a.url::attr(href)')


def next_page_url_fn_selector(s, r):
    # return r.xpath("//a[contains(.//text(), 'Next')]/@href")
    return r.xpath("//a[contains(.//text(), 'Next')]/@href")


class IndexItemSpiderExample(IndexItemSpider):
    name = "index-item-example"
    allowed_domains = ['www.destinationhonda.ca']
    start_urls = ['http://www.destinationhonda.ca/used-inventory/index.htm']
    ajax = True

    items_selector = items_selector
    item_url_selector = 'a.url::attr(href)'

    index_attrs = {'transmission': '.last dd:nth-child(6)'}
    item_attrs = {'name': '.ddc-page-title'}

    next_page_url_selector = next_page_url_fn_selector

    loader = CustomLoader

    pages_limit = 1