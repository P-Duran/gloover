from typing import List, Generator, Optional

from pymongo.errors import BulkWriteError

from gloover_model.database_instance import DatabaseInstance
from gloover_model.exceptions.document_already_exists_exception import DocumentAlreadyExistsException
from gloover_model.serialization.feature_sentence import FeatureSentence
from gloover_model.serialization.product import Product
from gloover_model.serialization.product_feature import ProductFeature
from gloover_model.serialization.review import Review
from gloover_model.serialization.review_stat import ReviewStat
from gloover_model.serialization.webpage import WebPage
from gloover_service.utils.logger import Logger


class DbManager:
    database = DatabaseInstance().database

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
        cls.database.reviews.insert_many(reviews)

    @classmethod
    def add_webpage(cls, webpage: WebPage):
        try:
            cls.database.websites.create_index([("company_name", -1)], unique=True)
            cls.database.websites.insert_one(webpage)
        except Exception as e:
            raise DocumentAlreadyExistsException("""Web page with "company_name": """ + webpage.company_name + """" 
            already exists""", e)

    @classmethod
    def add_product(cls, product: Product):
        try:
            cls.database.products.create_index([("asin", -1)], unique=True)
            cls.database.products.insert_one(product)
        except Exception as e:
            raise DocumentAlreadyExistsException("""Product with "asin": """ + product.asin + """" 
            already exists""", e)

    @classmethod
    def get_reviews(cls, asin=None, from_date=None, to_date=None, limit=0, page=1) -> List[Review]:
        search_filter = {}
        if asin is not None:
            search_filter["asin"] = asin
        if from_date and to_date:
            search_filter["date"] = {"$gte": from_date, "$lt": to_date}
        skips = limit * (page - 1)
        cursor = cls.database.reviews.find(search_filter).skip(skips).limit(limit)
        return [Review.from_json(review) for review in cursor]

    @classmethod
    def get_review_by_id(cls, id) -> Optional[Review]:
        search_filter = {"id": id}

        reviews = cls.database.reviews.find(search_filter)
        for review in reviews:
            return Review.from_json(review)

        return None

    @classmethod
    def get_products(cls, asin=None) -> List[Product]:
        search_filter = None
        if asin is not None:
            search_filter = {'asin': asin}
        products = cls.database.products.find(search_filter)
        Logger.log_warning(products)
        return [Product.from_json(product) for product in products]

    @classmethod
    def get_collection_statistics(cls, collection: str):
        return cls.database.command('collStats', collection)

    @classmethod
    def get_asin_reviews_stats(cls):
        results = cls.database.reviews.aggregate([{
            "$group": {
                "_id": "$asin",
                "negative_reviews": {"$sum": {"$cond": [{"$lte": ["$polarity", 2.5]}, 1, 0]}},
                "positive_reviews": {"$sum": {"$cond": [{"$gt": ["$polarity", 2.5]}, 1, 0]}}
            }
        }])
        for r in results:
            yield ReviewStat.from_json(r)

    @classmethod
    def get_feature_sentences_stats(cls, asin=None):
        aggregate_filters = [{
            "$group": {
                "_id": "$feature_id",
                "negative": {"$sum": {"$cond": [{"$lte": ["$polarity", 0.5]}, 1, 0]}},
                "positive": {"$sum": {"$cond": [{"$gt": ["$polarity", 0.5]}, 1, 0]}}
            }
        }]
        if asin is not None:
            aggregate_filters.insert(0, {"$match": {"asin": asin}})
        results = cls.database.feature_sentences.aggregate(aggregate_filters)
        for r in results:
            yield r

    @classmethod
    def get_product_features(cls, asin=None) -> List[ProductFeature]:
        search_filter = None
        if asin is not None:
            search_filter = {'asin': asin}
        features = cls.database.features.find(search_filter)
        return [ProductFeature.from_json(feature) for feature in features]

    @classmethod
    def add_product_features(cls, features: List[ProductFeature]):
        try:
            cls.database.features.create_index([("asin", -1), ("word", -1)], unique=True)
            cls.database.features.insert_many(features, ordered=False)
            return [f.id for f in features]
        except BulkWriteError as e:
            Logger.log_warning(e.details["writeErrors"][0]['errmsg'])
            duplicated = [error["op"]["id"] for error in e.details["writeErrors"]]
            return [f.id for f in features if f.id not in duplicated]

    @classmethod
    def get_product_feature_sentences(cls, asin=None, from_date=None, to_date=None, feature_id=None, limit=0, page=1) -> List[FeatureSentence]:
        search_filter = {}
        if asin is not None:
            search_filter["asin"] = asin
        if feature_id is not None:
            search_filter["feature_id"] = feature_id
        if from_date and to_date:
            search_filter["date"] = {"$gte": from_date, "$lt": to_date}
        skips = limit * (page - 1)
        cursor = cls.database.feature_sentences.find(search_filter).skip(skips).limit(limit)
        return [FeatureSentence.from_json(fs) for fs in cursor]

    @classmethod
    def add_feature_sentences(cls, feature_sentences: Generator):
        try:
            cls.database.feature_sentences.create_index(
                [("sentence", -1), ("review_id", -1), ("feature_id", -1)],
                unique=True)
            inserted = cls.database.feature_sentences.insert_many(feature_sentences, ordered=False)
            return 'ok', inserted.inserted_ids
        except BulkWriteError as e:
            Logger.log_warning(e.details["writeErrors"])
            return 'error', e.details["writeErrors"]
