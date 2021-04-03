from flask import Blueprint, jsonify, request

from gloover_model.exceptions.null_request_args_exception import NullRequestArgsException
from gloover_service.database_service import DatabaseService

database_api = Blueprint('database_api', __name__)


@database_api.route('/reviews', methods=['GET'])
def get_reviews():
    limit = int(request.args.get('limit', 1000))
    page = int(request.args.get('page', 1))
    asin = request.args.get('asin', None)
    _reviews, _pagination = DatabaseService.get_reviews(asin, limit, page)
    return jsonify(
        items=_reviews,
        pagination=_pagination
    )


@database_api.route('/products', methods=['GET'])
def get_products():
    products = DatabaseService.get_products()
    return jsonify(
        items=products,
    )


@database_api.route('/products/<asin>', methods=['GET'])
def get_product(asin):
    products = DatabaseService.get_products(asin)
    return jsonify(
        items=products,
    )


@database_api.route('/features/generate', methods=['POST'])
def generate_features():
    asin = request.form.get('product_asin')
    if not asin:
        raise NullRequestArgsException("product_asin form param can not be null")
    data = DatabaseService.generate_product_features(asin)
    return jsonify(data=data)


@database_api.route('/features/update', methods=['PUT'])
def update_features():
    asin = request.form.get('product_asin')
    if not asin:
        raise NullRequestArgsException("product_asin form param can not be null")
    data = DatabaseService.update_product_features(asin)
    return jsonify(data=data)


@database_api.route('/features/sentences/update', methods=['PUT'])
def update_feature_sentences():
    asin = request.form.get('product_asin')
    if not asin:
        raise NullRequestArgsException("product_asin form param can not be null")
    data = DatabaseService.update_product_feature_sentences(asin)
    return jsonify(data=data)
