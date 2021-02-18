import asyncio
import json

import requests
from requests import PreparedRequest

from gloover_model.db_manager import DbManager
from gloover_model.serialization.database.review import Review
from gloover_model.serialization.database.webpage import WebPage
from gloover_service.utils.logger import Logger


class ScraperService:
    _scraper_url = 'http://gloover_scraper:9080/crawl.json'

    @classmethod
    def scrap_url(cls, url, max_requests):
        asyncio.run(cls._scrap_url_task(url, max_requests))

    @classmethod
    async def _scrap_url_task(cls, url, max_requests):
        params = {'spider_name': 'amazon', 'url': url, 'max_requests': max_requests}
        req = PreparedRequest()
        req.prepare_url(cls._scraper_url, params)
        response = requests.get(url, params=params)
        print(response.text)
        json_response = json.loads(response.text)
        reviews = [Review.from_json(review) for review in json_response['url']['items']]
        DbManager.add_reviews(reviews, WebPage("amazon", "www.amazon.com", 5))