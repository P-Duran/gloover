from math import ceil
from typing import List, Tuple

from gloover_model.db_manager import DbManager
from gloover_model.exceptions.no_results_found_exception import NoResultsFoundException
from gloover_model.feature_extractor import FeatureExtractor
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
    def update_product_features(cls, asin):
        reviews = DbManager.get_reviews(asin)
        if len(reviews) == 0:
            raise NoResultsFoundException("There are no results for asin '" + asin + "'")
        simple_features, complex_features = FeatureExtractor.extract_features(reviews=reviews, product_asin=asin)
        feature_sentences = FeatureExtractor.extract_feature_sentences(simple_features, complex_features,
                                                                       reviews=reviews)
        DbManager.add_product_features(simple_features)
        DbManager.add_product_features(complex_features)
        DbManager.add_feature_sentences(feature_sentences)
        return "ok"
