# -*- coding: utf-8 -*-
import re

import scrapy
import os
import selectorlib
from dateutil import parser as dateparser


class AmazonSpider(scrapy.Spider):
    _COUNTRY_DATE_PATTERN = '.* in (the )?(?P<country>[a-zA-Z ]*) on (?P<date>.*)'
    _POLARITY_PATTERN = '(?P<polarity>[0-9//.]+)[a-z ]*(?P<maxPolarity>[0-9//.]+)[a-z ]*'

    name = 'amazon'
    allowed_domains = ['amazon.com']
    start_urls = [
        ]

    product_page_extractor = selectorlib.Extractor.from_yaml_file(
        os.path.join(os.path.dirname(__file__), '../configurations/amazon/review.yml'))

    def __init__(self, url='', *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]

    def parse(self, response):
        # Extract data using Extractor
        data = self.product_page_extractor.extract(response.text)

        if 'next_page' in data:
            yield scrapy.Request("https://www.amazon.com" + data['next_page'], callback=self.parse,)
        if 'reviews' in data:
            for review in data['reviews']:
                yield from self.create_review(data['product_title'], review)

    def create_review(self, product_name, unprocessed_review):
        polarity_match = re.search(self._POLARITY_PATTERN, unprocessed_review['rating'])
        country_date_match = re.search(self._COUNTRY_DATE_PATTERN, unprocessed_review['date'])
        try:
            country = country_date_match.group('country')
            date = dateparser.parse(country_date_match.group('date')).strftime('%d %b %Y')
            print(country, date)
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
                          'author': unprocessed_review['author'], 'polarity': polarity, 'maxPolarity': max_polarity}
        print(product_review)
        yield product_review
