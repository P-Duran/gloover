from flask import Blueprint, jsonify, request

from gloover_service.scraper_service import ScraperService

scraper_api = Blueprint('scraper_api', __name__)
scraper_service = ScraperService()


@scraper_api.route('/crawl')
def crawl_url():
    url = request.form.get('url')
    max_requests = request.form.get('max_requests')
    spider = request.form.get('spider_name')
    trigger = request.form.get('trigger')
    trigger_option = request.form.get('trigger_option')

    res = ScraperService.scrap_url(spider, url, max_requests, trigger, trigger_option)
    return jsonify(scraper_response=res)


@scraper_api.route('/notify/<scraper_id>', methods=['POST'])
def notify(scraper_id):
    res = ScraperService.get_scraped_items(scraper_id)
    return jsonify(staus=res)
