# -*- coding: utf-8 -*-
import os
import re
from urllib.parse import urlparse

import scrapy
import selectorlib
from dateutil import parser as dateparser


class AmazonSpider(scrapy.Spider):
    _COUNTRY_DATE_PATTERN = '.* in (the )?(?P<country>[a-zA-Z ]*) on (?P<date>.*)'
    _POLARITY_PATTERN = '(?P<polarity>[0-9//.]+)[a-z ]*(?P<maxPolarity>[0-9//.]+)[a-z ]*'
    requests = 0
    name = 'amazon'
    allowed_domains = ['amazon.com']
    start_urls = []
    product_page_extractor = selectorlib.Extractor.from_yaml_file(
        os.path.join(os.path.dirname(__file__), '../configurations/amazon/review.yml'))

    def __init__(self, url='', max_requests=3, **kwargs):

        print(url)
        self.start_urls = [url]
        self.max_requests = int(max_requests)
        self.domain = urlparse(url).netloc
        super().__init__(**kwargs)

    def parse(self, response):
        # Extract data using Extractor
        data = self.product_page_extractor.extract(response.text)
        self.requests += 1
        if 'next_page' in data and self.requests <= self.max_requests:
            yield scrapy.Request("https://" + self.domain + data['next_page'], self.parse, meta={
                'proxy': "http://scraperapi:91f827d26c173d7f2c6b8d458e57ff6b@proxy-server.scraperapi.com:8001"})
        if 'reviews' in data:
            for review in data['reviews']:
                yield from self.create_review(data['product_title'], review)

    def create_review(self, product_name, unprocessed_review):
        polarity_match = re.search(self._POLARITY_PATTERN, unprocessed_review['rating'])
        country_date_match = re.search(self._COUNTRY_DATE_PATTERN, unprocessed_review['date'])
        try:
            country = country_date_match.group('country')
            date = dateparser.parse(country_date_match.group('date')).strftime('%d %b %Y')
        except Exception:
            country = unprocessed_review['date']
            date = unprocessed_review['date']
        try:
            polarity = polarity_match.group('polarity')
            max_polarity = polarity_match.group('maxPolarity')
        except Exception:
            polarity = unprocessed_review['rating']
            max_polarity = unprocessed_review['rating']
        product_review = {'productName': product_name, 'title': unprocessed_review['title'],
                          'text': unprocessed_review['content'], 'date': date, 'country': country,
                          'author': unprocessed_review['author'], 'polarity': polarity, 'maxPolarity': max_polarity,
                          "domain": self.domain}
        print(self.domain)
        yield product_review
