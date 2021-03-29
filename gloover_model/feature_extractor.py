from typing import List, Tuple

from gloover_model.serialization.product_feature import ProductFeature
from gloover_model.serialization.review import Review
from gloover_model.services.feature_extractor.feature_selector import feature_selector
from gloover_model.services.feature_extractor.sentence_extractor import sentence_extractor


class FeatureExtractor(object):

    @classmethod
    def extract_features(cls, product_asin: str, reviews: List[Review]) -> Tuple[
        List[ProductFeature], List[ProductFeature]]:
        if not all(review.asin == product_asin for review in reviews):
            raise Exception("The reviews are not from the same product with asin '" + product_asin + "'")
        simple_features, complex_features = feature_selector(product_asin, reviews)
        return simple_features, complex_features

    @classmethod
    def extract_feature_sentences(cls, simple_features: List[ProductFeature], complex_features: List[ProductFeature],
                                  reviews: List[Review]):
        feature_sentences = sentence_extractor(reviews, simple_features, complex_features)
        return feature_sentences
