import json

import requests

from gloover_model.db_manager import DbManager
from gloover_model.serialization.database.review import Review
from gloover_model.serialization.database.webpage import WebPage
from gloover_service.utils.network import NetworkUtils


class ScraperService:
    _scraper_url = 'http://gloover_scraper:9080/data'

    @classmethod
    def scrap_url(cls, url, max_requests):
        cls._scrap_url_task("", url, max_requests)

    @classmethod
    def _scrap_url_task(cls, spider, url, max_requests):
        # params = {'spider_name': spider, 'url': url, 'max_requests': max_requests}
        # req = PreparedRequest()
        # req.prepare_url(cls._scraper_url, params)
        # response = requests.get(url, params=params)
        response = requests.get(cls._scraper_url)
        json_response = json.loads(response.text)
        domain = NetworkUtils.extract_domain(url)
        print(domain)
        company_name = NetworkUtils.extract_company_name(url)
        reviews = [Review.from_json(review) for
                   review in json_response['data']]
        DbManager.add_reviews(reviews, WebPage(company_name, domain, 5))
