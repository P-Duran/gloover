import json

import requests

from gloover_model.db_manager import DbManager
from gloover_model.serialization.product import Product
from gloover_model.serialization.review import Review
from gloover_model.serialization.webpage import WebPage
from gloover_service.utils.network import NetworkUtils


class ScraperService:
    _scraper_url = 'http://gloover_scraper:9080/'

    @classmethod
    def scrap_url(cls, spider, url, max_requests, trigger, trigger_option):
        body_form = {"url": (None, url), "max_requests": (None, max_requests), "spider_name": (None, spider),
                     "trigger": (None, trigger),
                     "trigger_option": (None, trigger_option)}
        response = requests.post(cls._scraper_url + "/scrape", files=body_form)
        return response.text

    @classmethod
    def get_scraped_items(cls, scraper_id):
        all_data_received = False
        page = 1
        while not all_data_received:
            get_params = {"limit": 1000, "page": page}
            response = requests.get(cls._scraper_url + "/containers/" + scraper_id, params=get_params)
            json_response = json.loads(response.text)
            all_data_received = json_response["pagination"]["last_page"] >= page or json_response["pagination"][
                "page_items"] == 0
            reviews = [Review.from_json(review) for
                       review in json_response['items'] if "text" in review]
            json_product = json_response['header_item']
            if json_product is not None:
                product = Product.from_json(json_product)
                DbManager.add_product(product)
            if len(reviews) > 0:
                domain = reviews[0].domain
                company_name = NetworkUtils.extract_company_name(domain)
                DbManager.add_reviews(reviews, WebPage(company_name, domain, 5))

        return "ok"
