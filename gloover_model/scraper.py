from urllib.parse import urlparse

import os
from scrapy.crawler import CrawlerProcess
from gloover_model.scraper.spiders.amazon_spider import AmazonSpider


class Scrapper:
    def __init__(self):
        self.path = "/tmp/scrapped_data"
        try:
            os.mkdir(self.path)
        except OSError:
            print("Creation of the directory %s failed" % self.path)
        else:
            print("Successfully created the directory %s " % self.path)

    def scrap(self, url):
        process = CrawlerProcess({'FEED_FORMAT': 'CSV',
                                  'FEED_URI': 'file:///' + self.path + '/export.csv'})
        domain = urlparse('http://www.example.test/foo/bar').netloc
        if domain.__contains__("amazon"):
            process.crawl(AmazonSpider,
                          url='https://www.amazon.com/HP-24mh-FHD-Monitor-Built/product-reviews/B08BF4CZSV/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews')
            process.start()
