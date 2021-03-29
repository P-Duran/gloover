from math import ceil
from typing import List, Tuple

from gloover_model.db_manager import DbManager
from gloover_model.exceptions.no_results_found_exception import NoResultsFoundException
from gloover_model.feature_extractor import FeatureExtractor
from gloover_model.serialization.product import Product
from gloover_model.serialization.product_feature import FeatureType
from gloover_model.serialization.review import Review


class DatabaseService(object):
    @classmethod
    def get_reviews(cls, asin, limit, page) -> Tuple[List[Review], dict]:
        total_reviews = DbManager.get_collection_statistics("reviews")['count']
        reviews = DbManager.get_reviews(asin, limit=limit, page=page)
        last_page = 1
        if limit > 0:
            last_page = ceil(total_reviews / limit)
        pagination = {"page": page, "last_page": last_page, "limit": limit,
                      "page_items": len(reviews),
                      "total_items": total_reviews}
        return reviews, pagination

    @classmethod
    def get_products(cls, asin=None) -> List[Product]:
        products = DbManager.get_products(asin)
        return products

    @classmethod
    def update_product_features(cls, asin):
        if asin is None:
            raise Exception("asin cant be null")

        reviews = DbManager.get_reviews(asin)
        if len(reviews) == 0:
            raise NoResultsFoundException("There are no results for asin '" + asin + "'")
        simple_features, complex_features = FeatureExtractor.extract_features(reviews=reviews, product_asin=asin)
        inserted_simple = DbManager.add_product_features(simple_features)
        inserted_complex = DbManager.add_product_features(complex_features)
        metadata = {
            "simple_features": {
                "detected": len(simple_features),
                "droped": len(simple_features) - len(inserted_simple)
            },
            "complex_features": {
                "detected": len(complex_features),
                "dropped": len(complex_features) - len(inserted_complex)
            }
        }
        return metadata

    @classmethod
    def update_product_feature_sentences(cls, asin):
        reviews = DbManager.get_reviews(asin)
        if len(reviews) == 0:
            raise NoResultsFoundException("There are no results for asin '" + asin + "'")
        features = DbManager.get_product_features(asin)
        simple_features = [f for f in features if f.type == FeatureType.SIMPLE]
        complex_features = [f for f in features if f.type == FeatureType.COMPLEX]
        feature_sentences = FeatureExtractor.extract_feature_sentences(simple_features, complex_features, reviews)
        inserted_sentences = DbManager.add_feature_sentences(feature_sentences)
        return len(inserted_sentences)
