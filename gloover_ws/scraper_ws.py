import time
from enum import Enum

import crochet
from flask import Blueprint, jsonify
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings

from gloover_model.scraper.spiders.amazon_spider import AmazonSpider

s = get_project_settings
crochet.setup()
scraper_api = Blueprint('scraper_api', __name__)

crawl_runner = CrawlerRunner()  # requires the Twisted reactor to run
output_data = []


class ScraperState(Enum):
    FREE = 1
    BUSY = 2


STATE = ScraperState.FREE


@scraper_api.route('/crawl')
def crawl_url():
    global STATE
    if STATE == ScraperState.FREE:
        STATE = ScraperState.BUSY
        scrape_with_crochet(baseURL="baseURL")

    time.sleep(20)  # Pause the function while the scrapy spider is running

    return jsonify(output_data)  # Returns the scraped data after being running for 20 seconds.


@scraper_api.route('/result')
def scraper_result():
    global output_data
    show_data = output_data
    if STATE == ScraperState.FREE:
        output_data = []
    return jsonify(
        scraper_state=STATE.name,
        result=show_data
    )


@crochet.run_in_reactor
def scrape_with_crochet(baseURL):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)

    eventual = crawl_runner.crawl(AmazonSpider)
    return eventual


def _crawler_result(item, response, spider):
    output_data.append(dict(item))


def finished_scrape(null):
    global STATE
    STATE = ScraperState.FREE
