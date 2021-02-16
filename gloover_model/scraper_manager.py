import csv
import os
from urllib.parse import urlparse
from scrapy.crawler import CrawlerRunner
from gloover_model.db_manager import DbManager
from gloover_model.scraper.spiders.amazon_spider import AmazonSpider
from gloover_service.objects.database.webpage import WebPage
from gloover_service.utils.logger import Logger


class ScraperManager(object):
    def __init__(self):
        self.db_manger = DbManager()
        self.path = "/tmp/scrapped_data"
        try:
            os.mkdir(self.path)
        except OSError:
            print("Creation of the directory %s failed" % self.path)
        else:
            print("Successfully created the directory %s " % self.path)

    def scrap(self, url):
        file_path = self.path + 'export.csv'
        process = CrawlerRunner({'FEED_FORMAT': 'CSV',
                                 'FEED_URI': 'export.csv'})
        domain = urlparse('http://www.example.test/foo/bar').netloc
        if domain.__contains__("amazon"):
            web_page = WebPage(company_name="amazon", domain=domain, max_score=5)
            eventual = process.crawl(AmazonSpider,
                                     url='https://www.amazon.com/HP-24mh-FHD-Monitor-Built/product-reviews/B08BF4CZSV/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews',
                                     max_iterations=1)
            eventual.addCallback(self.finished_scrape)

        # self.db_manger.add_reviews([Review.from_json(r) for r in reviews], web_page)

    def finished_scrape(self):
        Logger.log_debug("SCRAPED COMPLETED")
        with open('export.csv', mode='r') as infile:
            reader = csv.reader(infile)
        reviews = {rows[0]: rows[1] for rows in reader}
        Logger.log_debug(str(reviews))
