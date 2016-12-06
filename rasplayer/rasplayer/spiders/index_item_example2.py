# -*- coding: utf-8 -*-
import scrapy
from scrapy.item import Item
from scrapy_splash import SplashRequest
from rasplayer.defaults import DefaultLoader, IndexItemSpider
from w3lib.html import remove_tags
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity, Compose


class CustomLoader(DefaultLoader):
    name_in = MapCompose(remove_tags, unicode.strip, unicode.upper)


class IndexItemSpiderExample(IndexItemSpider):
    name = "index-item-example2"
    allowed_domains = ['theprovince.com']
    start_urls = ['http://theprovince.com/category/news/local-news']
    ajax = True

    items_selector = '.top-headline article, .second-row-list article'
    item_url_selector = 'header .entry-title a::attr(href)'

    index_attrs = {'title': 'header .entry-title a'}
    item_attrs = {'author': 'article .entry-details .author-wrap',
                  'image_src': 'article .post-image::attr(src)',
                  'body': 'article .article-body #page1'}

    # loader = CustomLoader
