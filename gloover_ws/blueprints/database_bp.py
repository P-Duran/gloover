from datetime import datetime

from flask import Blueprint, jsonify, request

from gloover_model.exceptions.request_args_exception import RequestArgsException
from gloover_model.serialization.ranking_type import RankingType
from gloover_service.database_service import DatabaseService

database_api = Blueprint('database_api', __name__)


@database_api.route('/reviews', methods=['GET'])
def get_reviews():
    limit = int(request.args.get('limit', 1000))
    page = int(request.args.get('page', 1))
    asin = request.args.get('asin', None)
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    if from_date or to_date:
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")

    _reviews, _pagination = DatabaseService.get_reviews(asin, from_date, to_date, limit, page)
    return jsonify(
        items=_reviews,
        pagination=_pagination
    )


@database_api.route('/reviews/<id>', methods=['GET'])
def get_review(id):

    _reviews = DatabaseService.get_review(id)
    return jsonify(
        items=_reviews
    )

@database_api.route('/reviews/statistics', methods=['GET'])
def get_review_stats():
    products = DatabaseService.get_reviews_stats()
    return jsonify(
        items=products,
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


@database_api.route('/features', methods=['GET'])
def get_features():
    asin = request.args.get('product_asin')
    data = DatabaseService.get_features(asin)
    return jsonify(items=data)


@database_api.route('/features/generate', methods=['POST'])
def generate_features():
    asin = request.form.get('product_asin')
    if not asin:
        raise RequestArgsException("product_asin form param can not be null")
    data = DatabaseService.generate_product_features(asin)
    return jsonify(items=data)


@database_api.route('/features/update', methods=['PUT'])
def update_features():
    asin = request.form.get('product_asin')
    if not asin:
        raise RequestArgsException("product_asin form param can not be null")
    data = DatabaseService.update_product_features(asin)
    return jsonify(items=data)


@database_api.route('/features/sentences/statistics', methods=['GET'])
def get_feature_sentences_stats():
    ranking_type = request.args.get('ranking_type', "DEFAULT")
    product_asin = request.args.get('product_asin')
    try:
        RankingType(ranking_type)
    except:
        raise RequestArgsException("ValueError: '" + ranking_type + "' is not a valid RankingType")

    data = DatabaseService.get_feature_sentence_stats(RankingType(ranking_type), product_asin)
    return jsonify(items=data)


@database_api.route('/features/sentences', methods=['GET'])
def get_feature_sentences():
    limit = int(request.args.get('limit', 1000))
    page = int(request.args.get('page', 1))
    asin = request.args.get('asin')
    feature_id = request.args.get('feature_id')

    _reviews, _pagination = DatabaseService.get_feature_sentences(asin, feature_id, limit, page)
    return jsonify(
        items=_reviews,
        pagination=_pagination
    )


@database_api.route('/features/sentences/update', methods=['PUT'])
def update_feature_sentences():
    asin = request.form.get('product_asin')
    if not asin:
        raise RequestArgsException("product_asin form param can not be null")
    data = DatabaseService.update_product_feature_sentences(asin)
    return jsonify(items=data)
