# -*- coding: utf-8 -*-
import json
import os
import re
import uuid
from urllib.parse import urlparse

import scrapy
import selectorlib
from dateutil import parser as dateparser


class AmazonSpider(scrapy.Spider):
    _COUNTRY_DATE_PATTERN = '.* in (the )?(?P<country>[a-zA-Z ]*) on (?P<date>.*)'
    _POLARITY_PATTERN = '(?P<polarity>[0-9//.]+)[a-z ]*(?P<maxPolarity>[0-9//.]+)[a-z ]*'
    _ASIN_PATTERN = "https://www.amazon.com(/[a-zA-Z0-9-]+)?/dp/(?P<asin>[A-Z0-9]+)"

    requests = 0
    name = 'amazon'
    allowed_domains = ['amazon.com']
    start_urls = []
    review_page_extractor = selectorlib.Extractor.from_yaml_file(
        os.path.join(os.path.dirname(__file__), '../templates/amazon/review.yml'))
    product_page_extractor = selectorlib.Extractor.from_yaml_file(
        os.path.join(os.path.dirname(__file__), '../templates/amazon/product.yml'))

    def __init__(self, url='', max_requests=3, **kwargs):

        print(url)
        self.start_urls = [url]
        self.max_requests = int(max_requests)
        self.domain = urlparse(url).netloc
        matcher = re.search(self._ASIN_PATTERN, url)
        self.asin = matcher.group('asin')
        super().__init__(**kwargs)

    def parse(self, response):
        product = self.product_page_extractor.extract(response.text)
        if 'link_to_all_reviews' in product:
            yield scrapy.Request("https://" + self.domain + product['link_to_all_reviews'], self.parse_review)
        if product:
            yield self.process_product(product)

    def parse_review(self, response):
        # Extract data using Extractor
        data = self.review_page_extractor.extract(response.text)
        self.requests += 1
        if 'next_page' in data and self.requests <= self.max_requests:
            yield scrapy.Request("https://" + self.domain + data['next_page'], self.parse_review)
        if 'reviews' in data:
            for review in data['reviews']:
                yield from self.create_review(data['product_title'], review)

    def create_review(self, product_name, unprocessed_review):
        polarity_match = re.search(self._POLARITY_PATTERN, unprocessed_review['rating'])
        country_date_match = re.search(self._COUNTRY_DATE_PATTERN, unprocessed_review['date'])
        try:
            country = country_date_match.group('country')
            date = dateparser.parse(country_date_match.group('date'))
        except Exception:
            country = unprocessed_review['date']
            date = unprocessed_review['date']
        try:
            polarity = polarity_match.group('polarity')
            max_polarity = polarity_match.group('maxPolarity')
        except Exception:
            polarity = unprocessed_review['rating']
            max_polarity = unprocessed_review['rating']
        product_review = {
            'id': str(uuid.uuid4()),
            'asin': self.asin,
            'title': unprocessed_review['title'],
            'text': unprocessed_review['content'],
            'date': date, 'country': country,
            'author': unprocessed_review['author'],
            'polarity': float(polarity),
            'max_polarity': float(max_polarity),
            "domain": self.domain
        }

        yield product_review

    def process_product(self, data):
        product = data.copy()
        del product['details']
        del product['link_to_all_reviews']
        if product['price'] is None:
            product['price'] = product['alternative_price']
            del product['alternative_price']
        product['images'] = list(json.loads(product['images']).keys())
        product['asin'] = self.asin
        polarity_match = re.search(self._POLARITY_PATTERN, product['rating'])
        polarity = polarity_match.group("polarity")
        product['rating'] = float(polarity)
        product['number_of_reviews'] = int(product['number_of_reviews']
                                           .replace("global ratings", "").replace(",", ""))
        return product
