# -*- coding: utf-8 -*-
import scrapy
from scrapy.item import Item
from rasplayer.defaults import DefaultLoader, IndexSpider
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity, Compose
from w3lib.html import remove_tags

attrs = {'time': 'td:nth-child(5)',
         'flightnumber': 'td:nth-child(2)',
         'airline': 'td:nth-child(1)',
         'to': 'td:nth-child(3)',
         'gate': 'td:nth-child(7)',
         'status': lambda l: l.add_css('status', 'td:nth-child(4)'),
         'extra_field': lambda l: l.add_value('extra_field', 'extra field value')
         }


class CustomLoader(DefaultLoader):
    status_in = MapCompose(remove_tags, unicode.strip, unicode.upper)


class IndexSpiderExample(IndexSpider):
    name = "index-example3"
    allowed_domains = ["flightview.com"]
    start_urls = ['http://tracker.flightview.com/FVAccess2/tools/fids/fidsDefault.asp?accCustId=FVWebFids&fidsId=20001&fidsInit=departures&fidsApt=SEA&fidsFilterAl=&fidsFilterArrap=']
    ajax = True
    attrs = attrs

    items_selector = '#fvData tr'

    # next_page_url_selector = ''

    loader = CustomLoader

    # items_per_page_limit = 10
    # items_limit = 2

    # pages_limit = 10

