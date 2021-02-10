# -*- coding: utf-8 -*-
import scrapy
import os
import selectorlib


class ScrapemeSpider(scrapy.Spider):
    name = 'scrapeme'
    allowed_domains = ['scrapeme.live']
    start_urls = ['http://scrapeme.live/shop/']
    # Create Extractor for listing page
    listing_page_extractor = selectorlib.Extractor.from_yaml_file(
        os.path.join(os.path.dirname(__file__), '../configurations/scrapme/ListingPage.yml'))
    # Create Extractor for product page
    product_page_extractor = selectorlib.Extractor.from_yaml_file(
        os.path.join(os.path.dirname(__file__), '../configurations/scrapme/ProductPage.yml'))

    def parse(self, response):
        # Extract data using Extractor
        data = self.listing_page_extractor.extract(response.text)
        if 'next_page' in data:
            yield scrapy.Request(data['next_page'], callback=self.parse,
                                 meta={'proxy': "http://scraperapi:91f827d26c173d7f2c6b8d458e57ff6b@proxy-server.scraperapi.com:8001"}
                                 )
        for p in data['product_page']:
            yield scrapy.Request(p,
                                 callback=self.parse_product,
                                 meta={
                                     'proxy': 'http://scraperapi:91f827d26c173d7f2c6b8d458e57ff6b@proxy-server.scraperapi.com:8001'}
                                 )

    def parse_product(self, response):
        # Extract data using Extractor
        product = self.product_page_extractor.extract(response.text)
        if product:
            yield product
