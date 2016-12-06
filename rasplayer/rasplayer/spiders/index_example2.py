# -*- coding: utf-8 -*-
import scrapy
from scrapy.item import Item
from scrapy.loader import ItemLoader
from rasplayer.defaults import DefaultLoader, IndexSpider
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity, Compose
from w3lib.html import remove_tags


# class CustomLoader(DefaultLoader):
#     image_urls_out = MapCompose(Identity)


class IndexSpiderExample2(IndexSpider):
    name = "index-example2"
    allowed_domains = ["shop.nordstrom.com"]
    start_urls = ['http://shop.nordstrom.com/c/womens-clothing']
    ajax = True
    attrs = {'name':        '.product-title',
             'price':       '.price',
             'image_urls':  '.product-photo::attr(src)',     # image_urls is a ImagesPipeline attribute
             'percent_off': '.percent-off'}

    items_selector = '.npr-product-module'

    next_page_url_selector = '.page-arrow.page-next .page-arrow-link::attr(href)'

    # loader = CustomLoader

    pages_limit = 1
    items_per_page_limit = 5

