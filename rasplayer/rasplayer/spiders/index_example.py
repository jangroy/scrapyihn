# -*- coding: utf-8 -*-
import scrapy
import time, datetime
from scrapy.item import Item
from rasplayer.defaults import DefaultLoader, IndexSpider
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity, Compose
from w3lib.html import remove_tags

attrs = {'time': 'td:nth-child(1)',
         'timestamp': 'td:nth-child(1)',
         'flightnumber': 'td:nth-child(3)',
         'airline': 'td:nth-child(4)',
         'from': 'td:nth-child(5)',
         'terminal': 'td:nth-child(6)',
         'gate': 'td:nth-child(7)',
         'status': lambda l: l.add_css('status', 'td:nth-child(8)'),
         'extra_field': lambda l: l.add_value('extra_field', 'extra field value')
         }


def str_date_to_str(str_date):
    datetime_obj = datetime.datetime.strptime(str_date, '%H:%M')
    return time.mktime(datetime_obj.timetuple())


class CustomLoader(DefaultLoader):
    status_in = MapCompose(remove_tags, unicode.strip, unicode.upper)
    timestamp_in = MapCompose(remove_tags, unicode.strip, str_date_to_str)


class IndexSpiderExample(IndexSpider):
    name = "index-example"
    allowed_domains = ["http://www.yvr.ca/en/passengers/flights/departing-flights"]
    start_urls = ['http://www.yvr.ca/en/passengers/flights/departing-flights']
    ajax = True
    attrs = attrs

    items_selector = 'tr.yvr-flights__row:not(.yvr-flights__row--hidden):not(.yvr-flights__row--button)'

    # next_page_url_selector = ''

    loader = CustomLoader

    items_limit = 50
    partition_size = 25

    # pages_limit = 10
    items_per_page_limit = 50



