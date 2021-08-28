import datetime
from math import ceil
from typing import List, Tuple, Dict, Optional

from gloover_model.db_manager import DbManager
from gloover_model.exceptions.no_results_found_exception import NoResultsFoundException
from gloover_model.feature_extractor import FeatureExtractor
from gloover_model.serialization.feature_sentence import FeatureSentence
from gloover_model.serialization.feature_sentence_stat import FeatureSentenceStat
from gloover_model.serialization.product import Product
from gloover_model.serialization.product_feature import FeatureType, ProductFeature
from gloover_model.serialization.ranking_type import RankingType
from gloover_model.serialization.review import Review
from gloover_model.singleton.singleton_meta import SingletonMeta
from gloover_model.utils.ranking_util import wilson_lower_bound


class DatabaseService(metaclass=SingletonMeta):
    @classmethod
    def get_reviews(cls, asin, from_date, to_date, limit, page) -> Tuple[List[Review], dict]:
        total_reviews = DbManager.get_collection_statistics("reviews")['count']
        reviews = DbManager.get_reviews(asin, from_date, to_date, limit=limit, page=page)
        last_page = 1
        if limit > 0:
            last_page = ceil(total_reviews / limit)
        pagination = {"page": page, "last_page": last_page, "limit": limit,
                      "page_items": len(reviews),
                      "total_items": total_reviews}
        return reviews, pagination

    @classmethod
    def get_review(cls, id) -> Optional[Review]:
        review = DbManager.get_review_by_id(id)

        return review

    @classmethod
    def get_reviews_stats(cls):
        result = DbManager.get_asin_reviews_stats()
        return list(result)

    @classmethod
    def get_products(cls, asin=None) -> Dict[str, Product]:
        result = {}
        for product in DbManager.get_products(asin):
            result[product.asin] = product
        return result

    @classmethod
    def get_features(cls, asin=None) -> List[ProductFeature]:
        return DbManager.get_product_features(asin)

    @classmethod
    def get_feature_sentences(cls, asin, from_date, to_date, feature_id, limit, page) -> Tuple[
        List[FeatureSentence], dict]:
        if asin is None:
            total_sentences = DbManager.get_collection_statistics("feature_sentences")['count']
        else:
            total_sentences = 0
            for stat in DbManager.get_feature_sentences_stats(asin):
                total_sentences += stat['positive'] + stat['negative']
        feature_sentences = DbManager.get_product_feature_sentences(asin, from_date, to_date, feature_id, limit, page)
        last_page = 1
        if limit > 0:
            last_page = ceil(total_sentences / limit)
        pagination = {"page": page, "last_page": last_page, "limit": limit,
                      "page_items": len(feature_sentences),
                      "total_items": total_sentences}
        return feature_sentences, pagination

    @classmethod
    def get_feature_sentence_stats(cls, ranking_type: RankingType = RankingType.DEFAULT, asin=None) \
            -> List[FeatureSentenceStat]:
        stats: List[FeatureSentenceStat] = []
        for stat in DbManager.get_feature_sentences_stats(asin):
            json = stat
            json['score'] = cls.__score_calculator(stat, ranking_type)
            stats.append(FeatureSentenceStat.from_json(json))

        return sorted(stats, key=lambda x: x.score, reverse=True)

    @classmethod
    def generate_product_features(cls, asin):
        if asin is None:
            raise Exception("asin cant be null")
        reviews = DbManager.get_reviews(asin)
        if len(reviews) == 0:
            raise NoResultsFoundException("There are no results for asin '" + asin + "'")

        simple_features, complex_features = FeatureExtractor.extract_features(reviews=reviews, product_asin=asin)
        feature_sentences = FeatureExtractor.extract_feature_sentences(asin, simple_features, complex_features, reviews)
        inserted_simple = DbManager.add_product_features(simple_features)
        inserted_complex = DbManager.add_product_features(complex_features)
        if len(simple_features) - len(inserted_simple) != 0 or len(complex_features) - len(inserted_complex) != 0:
            raise Exception("The features for asin '" + asin + "' are already created")
        inserted_sentences = DbManager.add_feature_sentences(feature_sentences)
        return 'ok'

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
        feature_sentences = FeatureExtractor.extract_feature_sentences(asin, simple_features, complex_features, reviews)
        inserted_sentences = DbManager.add_feature_sentences(feature_sentences)
        return len(inserted_sentences)

    @classmethod
    def __score_calculator(cls, data, ranking_type: RankingType):
        if ranking_type == RankingType.DEFAULT:
            return datetime.datetime.now().timestamp() / datetime.datetime.max.replace(
                tzinfo=datetime.timezone.utc).timestamp()
        elif ranking_type == RankingType.WILSON:
            return wilson_lower_bound(data['positive'], data['positive'] + data['negative'])
