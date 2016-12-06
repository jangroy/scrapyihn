import scrapy
from scrapy_splash import SplashRequest
from scrapy.item import Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity, Compose
from w3lib.html import remove_tags


class DefaultSpider(scrapy.Spider):
    pages_processed = 0
    pages_limit = 10000
    items_per_page_limit = 10000
    items_limit = 999999
    partition_size = 1

    def start_requests(self):
        for url in self.start_urls:
            # R = SplashRequest if self.ajax else scrapy.Request
            # yield R(url, callback=self.parse)
            yield SplashRequest(url, callback=self.parse, args={'wait': 1})


class DefaultLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, unicode.strip)
    default_output_processor = TakeFirst()

    image_urls_out = Identity()


def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def get_item_class(attrs):
    attrs_def = {}
    for attr in attrs:
        attrs_def[attr] = scrapy.Field()

    # Adds the attribute 'images' if image_urls is given
    if attrs.get('image_urls'):
        attrs_def['images'] = scrapy.Field()

    # Adds the attribute 'files' if file_urls is given
    if attrs.get('file_urls'):
        attrs_def['files'] = scrapy.Field()

    return type('Item', (Item,), attrs_def)


def get_loader_class(s):
    if hasattr(s, 'loader'):
        return s.loader
    else:
        return DefaultLoader


def get_items(s, response):
    if not hasattr(s, 'items_selector'):
        raise ValueError('Error: No items_selector was defined on the class')

    items_selector = s.items_selector

    # CSS selector
    if type(items_selector) is str:
        return response.css(items_selector)

    # Function selector
    else:
        return items_selector(response)


def get_next_page_url(s, response):
    if hasattr(s, 'next_page_url_selector'):
        selector = s.next_page_url_selector

        # CSS selector
        if type(selector) is str:
            return response.css(selector).extract_first()

        # Function selector
        else:
            return selector(response).extract_first()


def get_item_url(s, item):
    if not hasattr(s, 'item_url_selector'):
        raise ValueError("Error: No item_url_selector attribute was found!")

    selector = s.item_url_selector

    # CSS selector
    if type(selector) is str:
        return item.css(selector).extract_first()

    # Function selector
    else:
        return selector(item).extract_first()


def load_attr(loader, attr, attr_selector):

    # CSS SELECTOR
    if type(attr_selector) is str:
        loader.add_css(attr, attr_selector)

    # FUNCTION SELECTOR
    else:
        attr_selector(loader)


def load_attrs(loader, attrs):
    for attr in attrs:
        load_attr(loader, attr, attrs[attr])


class IndexSpider(DefaultSpider):
    def parse(self, response):
        self.pages_processed += 1
        if self.pages_processed <= self.pages_limit:
            items = get_items(self, response)
            next_page = get_next_page_url(self, response)
            loader_class = get_loader_class(self)
            attrs = self.attrs

            # print("self.loader:", self.loader)

            # Defines the ItemClass
            item_class = get_item_class(attrs)

            for item in items[:self.items_per_page_limit]:
                # Retrieves the ItemLoader
                loader = loader_class(item=item_class(), selector=item)

                # Loads the item attributes into the loader
                load_attrs(loader, attrs)
                yield loader.load_item()

            if next_page is not None:
                next_page = response.urljoin(next_page)
                print("***** next page url:", next_page, ", pages processed:", self.pages_processed)
                yield SplashRequest(next_page, callback=self.parse, args={'wait': 1})


class IndexItemSpider(DefaultSpider):
    def parse(self, response):
        self.pages_processed += 1
        if self.pages_processed <= self.pages_limit:
            index_attrs = self.index_attrs
            next_page = get_next_page_url(self, response)

            # Defines the index_class and loader_class
            index_class = get_item_class(index_attrs)
            loader_class = get_loader_class(self)

            for item in get_items(self, response)[:self.items_per_page_limit]:

                # Retrieves the ItemLoader
                loader = loader_class(item=index_class(), selector=item)

                # Loads the index attributes into the loader
                load_attrs(loader, index_attrs)

                url = get_item_url(self, item)

                if url is not None:
                    url = response.urljoin(url)
                    request = SplashRequest(url, callback=self.parse_item, meta={'item': loader.load_item()}, args={'wait': 1})
                    # request.meta['item'] = loader.load_item()
                    yield request
                else:
                    yield loader.load_item()

            if next_page is not None:
                next_page = response.urljoin(next_page)
                print("***** next page url:", next_page, ", pages processed:", self.pages_processed)
                yield SplashRequest(next_page, callback=self.parse, args={'wait': 1})

    def parse_item(self, response):
        # print("In parse-item!, item:", response.meta['item'])

        attrs = merge_dicts(self.item_attrs, self.index_attrs)

        # Defines the index_class and loader_class
        item_class = get_item_class(attrs)
        loader_class = get_loader_class(self)
        loader = loader_class(item=item_class(), selector=response)
        load_attrs(loader, attrs)

        # for attr in response.meta['item']:
        #     print("Attr:", attr, ":", response.meta['item'][attr])
        #     loader.add_value(attr, response.meta['item'][attr])

        yield merge_dicts(loader.load_item(), response.meta['item'])
