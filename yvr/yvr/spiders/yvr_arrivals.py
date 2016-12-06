# -*- coding: utf-8 -*-
import scrapy


class YvrArrivalsSpider(scrapy.Spider):
    name = "yvr-arrivals"
    allowed_domains = ["http://localhost:8050/render.html?url=http://www.yvr.ca/en/passengers/flights/arriving-flights"]
    start_urls = ['http://localhost:8050/render.html?url=http://www.yvr.ca/en/passengers/flights/arriving-flights']

    def parse(self, response):
        for flight in response.css(".yvr-flights__row:not(.yvr-flights__row-hidden):not( .yvr-flights__row--button)"):
            yield {
                'time': flight.css('td:nth-child(1) span::text').extract_first(),
                'id': flight.css('td:nth-child(3)::text').extract_first(),
                'airline': flight.css('td:nth-child(4)::text').extract_first(),
                'from': flight.css('td:nth-child(5)::text').extract_first(),
                'terminal': flight.css('td:nth-child(6)::text').extract_first().strip(),
                'gate': flight.css('td:nth-child(7)::text').extract_first(),
                'status': flight.css('td:nth-child(8) span::text').extract_first()
            }
