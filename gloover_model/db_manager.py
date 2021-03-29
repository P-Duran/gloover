from typing import List, Generator

from pymongo.errors import BulkWriteError

import gloover_ws.app
from gloover_model.exceptions.document_already_exists_exception import DocumentAlreadyExistsException
from gloover_model.serialization.product import Product
from gloover_model.serialization.product_feature import ProductFeature
from gloover_model.serialization.review import Review
from gloover_model.serialization.webpage import WebPage
from gloover_service.utils.logger import Logger


class DbManager:
    @classmethod
    def add_reviews(cls, reviews: List[Review], webpage: WebPage):
        if len(reviews) == 0:
            Logger.log_warning("The reviews are empty")
            return
        if not all([review.domain == reviews[0].domain for review in reviews]):
            raise Exception("The reviews are not from the same source")
        try:
            cls.add_webpage(webpage)
        except DocumentAlreadyExistsException:
            Logger.log_warning("Webpage already exists")
        gloover_ws.app.db.reviews.insert_many(reviews)

    @classmethod
    def add_webpage(cls, webpage: WebPage):
        try:
            gloover_ws.app.db.websites.create_index([("company_name", -1)], unique=True)
            gloover_ws.app.db.websites.insert_one(webpage)
        except Exception as e:
            raise DocumentAlreadyExistsException("""Web page with "company_name": """ + webpage.company_name + """" 
            already exists""", e)

    @classmethod
    def add_product(cls, product: Product):
        try:
            gloover_ws.app.db.products.create_index([("asin", -1)], unique=True)
            gloover_ws.app.db.products.insert_one(product)
        except Exception as e:
            raise DocumentAlreadyExistsException("""Product with "asin": """ + product.asin + """" 
            already exists""", e)

    @classmethod
    def get_reviews(cls, asin=None, limit=0, page=1) -> List[Review]:
        search_filter = None
        if asin is not None:
            search_filter = {'asin': asin}
        skips = limit * (page - 1)
        cursor = gloover_ws.app.db.reviews.find(search_filter).skip(skips).limit(limit)
        return [Review.from_json(review) for review in cursor]

    @classmethod
    def get_products(cls, asin=None) -> List[Product]:
        search_filter = None
        if asin is not None:
            search_filter = {'asin': asin}
        products = gloover_ws.app.db.products.find(search_filter)
        Logger.log_warning(products)
        return [Product.from_json(product) for product in products]

    @classmethod
    def get_collection_statistics(cls, collection: str):
        return gloover_ws.app.db.command('collStats', collection)

    @classmethod
    def add_product_features(cls, features: List[ProductFeature]):
        try:
            gloover_ws.app.db.features.create_index([("asin", -1), ("word", -1)], unique=True)
            gloover_ws.app.db.features.insert_many(features, ordered=False)
            return [f.id for f in features]
        except BulkWriteError as e:
            Logger.log_warning(e.details["writeErrors"][0]['errmsg'])
            duplicated = [error["op"]["id"] for error in e.details["writeErrors"]]
            return [f.id for f in features if f.id not in duplicated]

    @classmethod
    def get_product_features(cls, asin: str) -> List[ProductFeature]:
        features = gloover_ws.app.db.features.find({"asin": asin})
        return [ProductFeature.from_json(f) for f in features]

    @classmethod
    def add_feature_sentences(cls, feature_sentences: Generator):
        try:
            gloover_ws.app.db.feature_sentences.create_index(
                [("sentence", -1), ("review_id", -1), ("start", -1), ("end", -1)],
                unique=True)
            inserted = gloover_ws.app.db.feature_sentences.insert_many(feature_sentences)
            return 'ok', inserted.inserted_ids
        except BulkWriteError as e:
            Logger.log_warning(e.details["writeErrors"])
            return 'error', e.details["writeErrors"]
