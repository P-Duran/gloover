import crochet
from flask import Blueprint, jsonify, request

from gloover_service.scraper_service import ScraperService

crochet.setup()
scraper_api = Blueprint('scraper_api', __name__)
scraper_service = ScraperService()


@scraper_api.route('/crawl')
def crawl_url():
    url = request.args.get('url')
    max_requests = request.args.get('max_requests')
    ScraperService.scrap_url(url, max_requests)
    return jsonify(staus="noice")
