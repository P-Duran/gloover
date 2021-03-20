from flask import Blueprint, jsonify, request

from gloover_model.exceptions.null_request_args_exception import NullRequestArgsException
from gloover_service.database_service import DatabaseService
from gloover_service.scraper_service import ScraperService

database_api = Blueprint('database_api', __name__)
scraper_service = ScraperService()


@database_api.route('/reviews', methods=['GET'])
def get_reviews():
    limit = int(request.args.get('limit', 1000))
    page = int(request.args.get('page', 1))
    _reviews, _pagination = DatabaseService.get_reviews("0", limit, page)
    return jsonify(
        items=_reviews,
        pagination=_pagination
    )


@database_api.route('/features/update', methods=['PUT'])
def update_features():
    asin = request.form.get('product_asin')
    if not asin:
        raise NullRequestArgsException("product_asin form param can not be null")
    return jsonify(status=DatabaseService.update_product_features(asin))
