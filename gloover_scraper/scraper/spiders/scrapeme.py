# -*- coding: utf-8 -*-
import scrapy
import os
import selectorlib


class ScrapemeSpider(scrapy.Spider):
    name = 'scrapeme'
    allowed_domains = ['scrapeme.live']
    start_urls = ['http://scrapeme.live/shop/']
    iterations = 0
    # Create Extractor for listing page
    listing_page_extractor = selectorlib.Extractor.from_yaml_file(
        os.path.join(os.path.dirname(__file__), '../templates/scrapme/ListingPage.yml'))
    # Create Extractor for product page
    product_page_extractor = selectorlib.Extractor.from_yaml_file(
        os.path.join(os.path.dirname(__file__), '../templates/scrapme/ProductPage.yml'))

    def parse(self, response):
        # Extract data using Extractor
        data = self.listing_page_extractor.extract(response.text)
        self.iterations+=1
        if 'next_page' in data and self.iterations < 3:
            yield scrapy.Request(data['next_page'], callback=self.parse
                                 )
        for p in data['product_page']:
            yield scrapy.Request(p,
                                 callback=self.parse_product

                                 )

    def parse_product(self, response):
        # Extract data using Extractor
        product = self.product_page_extractor.extract(response.text)
        if product:
            yield product
