from typing import List

from pymongo.errors import BulkWriteError

import gloover_ws.app
from gloover_model.exceptions.document_already_exists_exception import DocumentAlreadyExistsException
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
    def get_reviews(cls, asin, limit=0, page=1) -> List[Review]:
        skips = limit * (page - 1)
        cursor = gloover_ws.app.db.reviews.find().skip(skips).limit(limit)
        return [Review.from_json(review) for review in cursor]

    @classmethod
    def get_collection_statistics(cls, collection: str):
        return gloover_ws.app.db.command('collStats', collection)

    @classmethod
    def add_product_features(cls, features: List[ProductFeature]):
        try:
            gloover_ws.app.db.features.create_index([("asin", -1), ("word", -1)], unique=True)
            gloover_ws.app.db.features.insert_many(features, ordered=False)
        except BulkWriteError:
            Logger.log_warning("ProductFeatures Duplicates found in MongoDB")

    @classmethod
    def add_feature_sentences(cls, feature_sentences):
        try:
            gloover_ws.app.db.feature_sentences.insert_many(feature_sentences)
        except Exception:
            Logger.log_warning("FeatureSentences could not be added to MongoDB")
